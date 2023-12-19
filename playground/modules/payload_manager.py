from django.core.files.uploadedfile import UploadedFile

from .audio_buffer import AudioBufferInMemory
class PayloadManager:
    """
    Manages the payload (nothing but audio file for processing)
    * Singleton
    How?
        - creates a payload-info
        - verify the payload-info against the user level policy
            * every user assigned to group of policies (usage-policy, priority-policy, etc.)
        - saves payload-info in database
            * saving the payload-info (valid audio file) makes sense for future propose
        - try adding to the payload-queue
            * payload-queue is a thread-safe queue
            * queue between producer and consumer
        - looks for results in result-queue same
            * same as payload-queue, but storing results from AI Service
        - after fetching the results then saves it to database
    """


    def process(self, file: UploadedFile, user_id: str) -> bool:
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
