from django.core.files.uploadedfile import UploadedFile, InMemoryUploadedFile

class AudioBufferInMemory:
    """Holds the buffer for processing.
    """
    file_name: str
    sizeInBytes: str
    buffer: str
    user_id: str
    transcribed: bool = False
    result: str = ''

    def __init__(self, file_name, size, buffer, user_id):
        self.file_name = file_name
        self.sizeInBytes = size
        self.buffer = buffer
        self.user_id = user_id

