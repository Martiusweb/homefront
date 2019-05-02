# coding: utf-8
from typing import Dict, IO, List, Optional, Union

import fnmatch
import glob
import logging
import os
import re
import shutil
import tarfile
import tempfile
import zipfile

import github
import packaging.version
import requests

import homefront

LOG = logging.getLogger(__name__)

ParsedVersion = Union[packaging.version.Version,
                      packaging.version.LegacyVersion]

Version = Union[str, ParsedVersion]


_ALL_MATCHER = f"[^{re.escape(os.path.sep)}]*"

_BUFFER_SIZE = 1024 * 8  # 8KiB

_NPM_REGISTRY_URL = "https://registry.npmjs.org"


def _translate_pattern(pattern: str) -> re.Pattern:
    # Make sure we don't match the path separator with the "*"
    # except for the last one. This is a bit ugly but it will be
    # sufficient for now.
    if pattern[-1] == os.path.sep:
        count = pattern.count("*")
        pattern += "*"
    else:
        count = 0

    regex = fnmatch.translate(pattern)
    regex = regex.replace(".*", _ALL_MATCHER, count)
    return re.compile(regex)


ExtractTarget = Dict[str, Optional[str]]


class Release:
    def __init__(self, required_version: str, artifact: str,
                 destination: Union[str, os.PathLike],
                 to_extract: Optional[ExtractTarget] = None):
        """
        to_extract is a dict of {patterns => destination}:

        The partern is a glob-like pattern where ``*`` is non-greedy, ``**`` is
        not supported. If the pattern ends with a ``/``, all the contents of
        the matching directory is extracted.

        destination is an optional destination for the files matching the
        patterns (ie: each matched pattern is moved under the destination). If
        None, the matched pattern is moved to the destination following the
        same structure of the archive.

        :param required_version: version of the package to get
        :param artifact: repository or artifact name
        :param destination: destination path
        :param to_extract: dict of pattern and destination of the files to
        extract
        :raise: packaging.version.InvalidVersion
        """
        version = parse_version(required_version)

        self.artifact: str = artifact
        self.name: str = artifact
        self.required_version: ParsedVersion = version
        self.release_version: Optional[ParsedVersion] = None
        self.destination: Union[str, os.PathLike] = destination
        self.to_extract: ExtractTarget = {
            "package/package.json": "package.json"
        }
        if to_extract:
            self.to_extract.update(to_extract)

    @property
    def url(self):
        raise NotImplementedError

    def is_best_candidate(self, version: Version) -> bool:
        version = parse_version(version)

        return (
            # A stable version is required
            not version.is_prerelease and
            version_matches(self.required_version, version) and
            # keep this version if it's more recent that the one we have
            (self.release_version is None or version > self.release_version)
        )

    def fetch(self, destination: Union[str, IO[bytes]]) -> None:
        """
        Download the release to the destination file.

        :param destination: destination of the archive
        """
        if isinstance(destination, str):
            destfile = open(destination, "wb")
        else:
            destfile = destination

        try:
            response = requests.get(self.url)
            if not response.ok:
                response.close()
                raise homefront.HomefrontException(
                    f"Failed to download {self.url}, HTTP response is "
                    f"{response.status_code}")

            for chunk in response.iter_content(chunk_size=_BUFFER_SIZE):
                destfile.write(chunk)
        finally:
            if isinstance(destination, str):
                destfile.close()

    def extract(self, source: Union[str, IO[bytes]],
                destination: Union[str, os.PathLike]) -> None:
        raise NotImplementedError

    def install(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempfile.NamedTemporaryFile() as archive:
                self.fetch(archive)
                archive.seek(0)

                self.extract(archive, tmpdir)

            for pattern, target in self.to_extract.items():
                matches = glob.glob(os.path.join(tmpdir, pattern))

                if target is not None and len(matches) > 1:
                    raise ValueError(
                        f"Ambiguous glob {pattern} can not be moved to "
                        f"{target} because there are multiple matches: "
                        f"{', '.join(matches)}")

                for src in matches:
                    if target is None:
                        dest = os.path.relpath(src, tmpdir)
                    else:
                        dest = target

                    dest = os.path.join(self.destination, target)

                    LOG.debug("installing %s to %s", src, dest)

                    if os.path.isfile(src):
                        # We are moving a file, ensure the parent directory
                        # exists first
                        os.makedirs(os.path.dirname(dest), exist_ok=True)
                    else:
                        # We are moving a whole directory
                        if os.path.isdir(dest):
                            shutil.rmtree(dest)

                    shutil.move(os.path.join(tmpdir, src), dest)


class GithubRelease(Release):
    def __init__(self, required_version: str, repo: str,
                 destination: Union[str, os.PathLike],
                 to_extract: Optional[Dict] = None):
        super().__init__(required_version, repo, destination, to_extract)
        self.release: Union[None, github.GitRelease.GitRelease, str] = None

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
        releases = api.get_repo(self.artifact).get_releases()

        for candidate in releases:
            try:
                version = parse_version(candidate.tag_name.lstrip("v"))
            except packaging.version.InvalidVersion as exc:
                LOG.debug("Failed to parse version %s: %s",
                          candidate.tag_name.lstrip('v'), exc)
                continue

            if self.is_best_candidate(version):
                self.release_version = version
                self.release = candidate

        if not self.release:
            raise ValueError(f"Could not find a release for {self.name} "
                             f"satisfying version >= {version}")

        return self.release

    @property
    def url(self):
        return self.get_github_release().zipball_url

    def extract(self, source: Union[str, IO[bytes]],
                destination: Union[str, os.PathLike]) -> None:
        extract_zip(source, destination, self.to_extract.keys())


class NpmRelease(Release):
    def __init__(self, required_version: str, project: str,
                 destination: Union[str, os.PathLike],
                 to_extract: Optional[Dict] = None):
        super().__init__(required_version, project, destination, to_extract)
        self.release_url: str = ""

    def get_npm_release_url(self) -> str:
        if self.release_url:
            return self.release_url

        response = requests.get(f"{_NPM_REGISTRY_URL}/{self.artifact}")

        if not response.ok:
            raise homefront.Error(f"Failed to fetch {self.artifact} metadata "
                                  "from npm registy")

        for candidate in response.json()["versions"].values():
            try:
                version = parse_version(candidate["version"])
            except packaging.version.InvalidVersion as exc:
                LOG.debug("Failed to parse version %s: %s",
                          candidate["version"], exc)
                continue

            if self.is_best_candidate(version):
                self.release_version = version
                self.release_url = candidate["dist"]["tarball"]

        if not self.release_url:
            raise ValueError(f"Could not find a release for {self.name} "
                             f"satisfying version >= {version}")

        return self.release_url

    @property
    def url(self) -> str:
        return self.get_npm_release_url()

    def extract(self, source: Union[str, IO[bytes]],
                destination: Union[str, os.PathLike]) -> None:
        extract_tar(source, destination, self.to_extract)


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


def extract_zip(source: Union[str, IO[bytes]],
                destination: Union[str, os.PathLike],
                patterns: List[str]) -> None:
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
                        LOG.debug("Extracting %s to %s", filename, destination)
                        archive.extract(filename, destination)
                        break


def extract_tar(source: Union[str, IO[bytes]],
                destination: Union[str, os.PathLike],
                patterns: List[str]) -> None:
    """
    extract contents from source to the destination.
    If patterns are provided, only files matching them are extracted.
    """
    if patterns:
        patterns = list(map(_translate_pattern, patterns))

    args = {("name" if isinstance(source, str) else "fileobj"): source}

    with tarfile.open(**args) as archive:
        if not patterns:
            archive.extractall(destination)
        else:
            for filename in archive.getnames():
                for pattern in patterns:
                    if pattern.match(filename):
                        LOG.debug("Extracting %s to %s", filename, destination)
                        archive.extract(filename, destination)
                        break
