import queue
import threading

from django.core.files.uploadedfile import UploadedFile

from common.modules.design_patterns import Singleton
from main.models import UserBase
from playground.models import PayloadInfo, PayloadStatus, PayloadRequestResponse



class PayloadExecutor(metaclass=Singleton):
    """
    Worker to execute payload(s)
        -   Looks for new item added to queue
    """
    __cancellation_token = False
    __payload_queue = queue.Queue()
    __result_queue = queue.Queue()
    __worker_thread: threading.Thread = None
    def __init__(self, executor_func):
        self.__executor_func = executor_func

    def start(self):
        """
        Start the working thread here
        """
        threading.Thread(target=self.__worker_thread_func(), daemon=True)

    def stop(self):
        pass

    def __worker_thread_func(self):
        """
        Actual worker thread func to execute the payload(s)
        """
        try:
            current_task = None
            while not self.__cancellation_token:
                try:
                    if self.__payload_queue.unfinished_tasks:
                        current_task = self.__payload_queue.get()
                        if current_task is not None:
                            print(f'Working on current task: {current_task}')
                            # main execution being called here:
                            if self.__executor_func(current_task):
                                print(f'Task execution result SUCCESS: {current_task}')
                            else:
                                print(f'Task execution result FAILURE: {current_task}')
                        else:
                            print(f'Skipping an empty task: {current_task}')
                except Exception as ex:
                    print(f"Inner scope exception raised {ex}")
        except Exception as ex:
            print(f"Outer scope exception raised {ex}")

class PayloadManager(metaclass=Singleton):
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
            status=PayloadStatus.SUCCESS_UPLOAD,
            audio_file_name=audio_file.name,
            message="NA",
        )
        payload_info.save()
        return payload_info

    def update_response(self,
                        payload,
                        upload_response: UploadResponse):
        upload_response.upload_success = True
        upload_response.errors_list.clear()
        upload_response

    # this acts like producer method
    def add_payload(self,
                    current_user: UserBase,
                    audio_file: UploadedFile,
                    upload_response: UploadResponse) -> bool:
        """
        Try to add the 'server-validated audio file' as payload to payload-queue
        """
        result: bool = False
        payload = self.__create_payload_info(current_user, audio_file)

        if payload is not None:
            self.process_payload(payload)


        return result


    # this acts like consumer method
    def process_payload(self, payload):
        pass

