# coding: utf-8
from typing import Optional, Union, IO, List

import fnmatch
import glob
import os
import re
import shutil
import tempfile
import zipfile

import packaging.version
import github
import requests

import homefront

_GITHUB_BOOTSTRAP_REPO = "twbs/bootstrap"
_ARCHIVE_DIRECTORIES_TO_EXTRACT = {
    # * is non-greedy, ** is not supported
    # if the pattern ends with a /, all the contents of the matching directory
    # is extracted
    # pattern: destination under the destination root (if none, not moved)
    "*bootstrap-*/scss/": "scss/bootstrap",
    "*bootstrap-*/js/src/": "js/bootstrap",
}

_BUFFER_SIZE = 1024 * 8  # 8KiB
_ALL_MATCHER = f"[^{re.escape(os.path.sep)}]*"


ParsedVersion = Union[packaging.version.Version,
                      packaging.version.LegacyVersion]

Version = Union[str, ParsedVersion]


def _translate_pattern(pattern: str) -> re.Pattern:
    # Make sure we don't match the path separator with the "*"
    # except for the last one. This is a bit ugly but it will be
    # sufficient for now.
    if pattern[-1] == os.path.sep:
        count = pattern.count("*")
        pattern += "*"
    else:
        count = None

    regex = fnmatch.translate(pattern)
    regex = regex.replace(".*", _ALL_MATCHER, count)
    return re.compile(regex)


class Release:
    """
    Represents a release to fetch from github.
    """
    def __init__(self, required_version: str, repo: str,
                 destination: Union[str, os.PathLike]):
        """
        :param required_version: version of the package to get
        :param repo: repository name (with owner)
        :raise: packaging.version.InvalidVersion
        """
        version = parse_version(required_version)

        self.repo: str = repo
        self.required_version: ParsedVersion = version
        self.release_version: Optional[ParsedVersion] = None
        self.release: Union[None, github.GitRelease.GitRelease, str] = None
        self.destination: Union[str, os.PathLike] = destination

    def get_github_release(self) -> github.GitRelease.GitRelease:
        """
        Return the highest github release of satisfying
        :attr:`required_version` in semver.

        :param version: required version, as a string
        :param repo: github repository name, in ``owner/repo`` form

        return a github release object
        """
        if self.release:
            return self.release

        api = github.Github()
        releases = api.get_repo(self.repo).get_releases()

        for candidate in releases:
            version = parse_version(candidate.tag_name.lstrip("v"))

            # A stable version is required
            if version.is_prerelease:
                continue

            if not version_matches(self.required_version, version):
                continue

            # keep this version if it's more recent that the one we have
            if (self.release_version is not None and
                    version < self.release_version):
                continue

            self.release_version = version
            self.release = candidate

        if not self.release:
            raise ValueError(f"Could not find a bootstrap release "
                             f"satisfying version >= {version}")

        return self.release

    def fetch_github_release(self, destination: Union[str, IO[bytes]],
                             url: Optional[str] = None) -> None:
        """
        Download the release to the destination file.

        :param destination: destination of the archive
        :param url: optional url, if not provided, use the release zipball url
        """
        if not url:
            url = self.get_github_release().zipball_url

        if isinstance(destination, str):
            destfile = open(destination, "wb")
        else:
            destfile = destination

        try:
            response = requests.get(url)
            if not response.ok:
                response.close()
                raise homefront.HomefrontException(
                    f"Failed to download {url}, HTTP response is "
                    f"{response.status_code}")

            for chunk in response.iter_content(chunk_size=_BUFFER_SIZE):
                destfile.write(chunk)
        finally:
            if isinstance(destination, str):
                destfile.close()

    @staticmethod
    def extract(source: Union[str, IO[bytes]],
                destination: Union[str, os.PathLike],
                *patterns: List[str]) -> None:
        """
        extract contents from source to the destination.
        If patterns are provided, only files matching them are extracted.
        """
        if patterns:
            patterns = list(map(_translate_pattern, patterns))

        with zipfile.ZipFile(source) as archive:
            if not patterns:
                archive.extractall(destination)
            else:
                for filename in archive.namelist():
                    for pattern in patterns:
                        if pattern.match(filename):
                            archive.extract(filename, destination)
                            break

    def install(self, url: Optional[str] = None) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempfile.NamedTemporaryFile() as archive:
                self.fetch_github_release(archive, url)
                archive.seek(0)

                self.extract(archive, tmpdir,
                             *_ARCHIVE_DIRECTORIES_TO_EXTRACT.keys())

            for pattern, target in _ARCHIVE_DIRECTORIES_TO_EXTRACT.items():
                matches = glob.glob(os.path.join(tmpdir, pattern))

                if target and len(matches) > 1:
                    raise ValueError(
                        f"Ambiguous glob {pattern} can not be moved to "
                        f"{target} because there are multiple matches: "
                        f"{', '.join(matches)}")

                for src in matches:
                    dest = os.path.join(self.destination, target or src)
                    if os.path.exists(dest):
                        shutil.rmtree(dest)

                    print(os.path.join(tmpdir, src), dest)
                    os.renames(os.path.join(tmpdir, src), dest)


def parse_version(version: Version) -> ParsedVersion:
    """
    Parse a version string or return the already parsed object.
    Assume that a ``release`` component is required.

    :param version: version
    :raise: packaging.version.InvalidVersion
    """
    if isinstance(version, str):
        result = packaging.version.parse(version)
    else:
        result = version

    if not result.release:
        raise packaging.version.InvalidVersion(
            f"Can not get a release from version {version}")

    return result


def version_matches(required: Version, candidate: Version) -> bool:
    """
    Return ``True`` if ``candidate`` is a version compatible with ``required``.

    Compatible means that they have the same major version, and that
    ``candidate`` is a release greater or equal to ``required``.
    """
    required = parse_version(required)
    candidate = parse_version(candidate)

    # The major version must be identical, and candidate must be above or equal
    # to the required version
    return (required.release[0] == candidate.release[0] and
            candidate >= required)


def download_bootstrap(version: str, destination: Union[str, os.PathLike]
                       ) -> None:
    release = Release(version, "twbs/bootstrap", destination)
    release.install()
