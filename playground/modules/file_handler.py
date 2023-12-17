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


def handle_file(file: UploadedFile, user_id: str) -> bool:
    """File Handler:
        -   Handles the uploaded file to AI server
        -   Perform basic sanity checks
        -   Keeps the audio clips in memory
    """
    result: bool = False
    buffer = file.read()
    if buffer is not None:
        obj = AudioBufferInMemory(file.name, file.size, buffer, user_id)

    return result
