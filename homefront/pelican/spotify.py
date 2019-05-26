# coding: utf-8
import festune.index
import festune.playlist

import pelican.signals
import pelican.generators


class SpotifyPlaylistGenerator(pelican.generators.Generator):
    playlists = None
    tracks = None

    def init(self):
        self.playlists = festune.index.FestonPlaylistsIndex()
        self.tracks = festune.index.TracksIndex()

    def load_playlists(self):
        self.playlists.add_all(festune.playlist.FestonPlaylist.load_all())

    def load_tracks(self):
        self.tracks.add_all(festune.playlist.PlaylistTrack.load_all())

    def generate_context(self):
        self.context["spotify"] = self

        # Load from disk
        self.load_playlists()
        self.load_tracks()

    def generate_output(self, writer):
        for playlist in self.playlists:
            writer.write_file(
                f"spotify/{playlist.year}-{playlist.month:02d}.html",
                self.get_template("spotify_playlist"),
                self.context, playlist=playlist,
                tracks=self.tracks.tracks_of(playlist).items())


def get_generators(_):
    return SpotifyPlaylistGenerator


def register():
    pelican.signals.get_generators.connect(get_generators)
    pelican.signals.generator_init.connect(SpotifyPlaylistGenerator.init)
