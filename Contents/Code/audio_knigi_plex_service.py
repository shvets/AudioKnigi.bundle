from audio_knigi_service import AudioKnigiService

from plex_storage import PlexStorage

class AudioKnigiPlexService(AudioKnigiService):
    def __init__(self):
        storage_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'audio_knigi.storage'))

        self.queue = PlexStorage(storage_name)

        self.queue.register_simple_type('author')
        self.queue.register_simple_type('performer')
        self.queue.register_simple_type('tracks')
