import queue
import threading

from django.core.files.uploadedfile import UploadedFile

from common.modules.design_patterns import Singleton
from main.models import UserBase
from playground.models import PayloadInfo, PayloadStatus, PayloadResponse
from .context_executor import ContextExecutor

__executor = ContextExecutor(None)


class ContextManager(metaclass=Singleton):
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

    def __create_payload_info(self,
                              current_user: UserBase,
                              audio_file: UploadedFile):
        payload_info = PayloadInfo(
            owner=current_user,
            status=PayloadStatus.UPLOADED,
            audio_file_name=audio_file.name,
            message="NA",
        )
        return payload_info

    def update_response(self,
                        payload,
                        upload_response: PayloadResponse):
        upload_response.upload_success = True
        upload_response.errors_list.clear()

    # this acts like producer method
    def try_add_payload(self,
                        current_user: UserBase,
                        audio_file: UploadedFile,
                        upload_response: PayloadResponse) -> bool:
        """
        Try to add the 'server-validated audio file' as payload to payload-queue
        """
        result: bool = False
        payload = self.__create_payload_info(current_user, audio_file)
        payload.is_latest = True
        payload.save()
        if payload is not None:
            result = True
            upload_response.file_name = payload.audio_file_name
            upload_response.uploaded_at = payload.uploaded_at
            upload_response.status = PayloadStatus.QUEUED

        return result

    # this acts like consumer method
    def process_payload(self, payload):
        pass

    def get_user_payloads(self,
                          user_id,
                          payload_collection: list):
        """
        Returns collection of PayloadRequestResponse
        -
        """
        col = PayloadInfo.objects.filter(owner=user_id).values()
        return col
