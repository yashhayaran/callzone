import queue
import threading
from common.modules.design_patterns import Singleton


class ContextExecutor(metaclass=Singleton):
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
