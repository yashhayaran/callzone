from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile, UploadedFile

'''Single place to hold the buffer reference of audio 
'''


class AudioBufferInMemory:
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


'''File Handler:
    -   Handles the uploaded file to server 
    -   Perform basic sanity checks 
    -   Keeps the audio clips in memory 
'''


def handle_file(file: UploadedFile, user_id: int) -> bool:
    result: bool = False
    buffer = file.read()
    if buffer is not None:
        obj = AudioBufferInMemory(file.name, file.size, buffer, user_id)

    return result
