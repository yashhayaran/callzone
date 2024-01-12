import json

from django.contrib.auth.models import User
from django.db import models
from django.http import JsonResponse
from django.utils import timezone

from common.models import uuid_generator
from main.models import UserBase

from django.utils.translation import gettext_lazy as _


class PayloadStatus(models.IntegerChoices):
    UNKNOWN = 0, 'UNKNOWN'
    UPLOADED = 1, 'UPLOADED'
    ACCEPTED = 2, 'ACCEPTED'
    QUEUED = 3, 'QUEUED'
    PROCESSING = 4, 'PROCESSING'
    FINISHED = 5, 'FINISHED'
    TRANSCRIBED = 6, 'TRANSCRIBED'
    FAILED = 7, 'FAILED'
    ERROR = 8, 'ERROR'


class PayloadResponse(models.Model):
    """
    PayloadResponse is client-side
        - create for new client-valid request
        - won't store in database
        - PayloadInfo compose
        - rendered as table row

    life-span of audio file:
    1. valid        - Waiting       - server validates the file
    2. queued       - Started       - file in queue to be processed by AI Service
    3. in-process   - Processing    - file is being transcribed
    4. finished     - Done          - file transcribed or not
    5. error        - Error         - any server related error internal error
    6. failed       - Failed        - failure due to policy breach, or can't find any word
    7. transcribed  - Success       - successfully generated transcribe

    JSON:
    {
        "unique_id" : <hex:str>
        "file_name" : <filename:str>,
        "file_size" : <mb:str>,
        "file_length" : <mm::ss:str>,
        "status" : <PayloadStatus:str>,
    }
    """
    status: PayloadStatus = PayloadStatus.UNKNOWN

    unique_id: str = "NA"
    file_name: str = "NA"
    uploaded_at: str = "NA"
    file_length: str = "NA"
    file_size: str = "NA"

    errors_list: list = list()

    def __str__(self):
        result: str = "{}"
        try:
            result = json.dumps(self, default=lambda o: o.__dict__)
        except Exception as ex:
            result = "{exception:" + str(ex) + "}"
        finally:
            return result


class PayloadInfo(models.Model):
    """
    PayloadInfo is main datastructure, holds the actual info in database
        - create for new valid request
        - can be stored in database
        - shared between server and black-box
        - holds audio file datastructure
        - delete when result is READY
    Represents payload info:
        audio_file_name
            -   user requests to process the audio file
                we usally keep that "in-memory" for privacy purpose
                just save the filename for user's reference
        status
            -   processing status of the file
                SUCCESS_TRANSCRIBE
                ERROR_UPLOAD_SERVER
                ERROR_INVALID_FILE_FORMAT
                ERROR_MAX_SIZE_REACHED
                ERROR_UNABLE_PROCESS
                ERROR_UNKNOWN
                FAIL_NO_TRANSCRIBE
        message
            -   message in case of error
        transcribe
            -   transcribe results for user
    """
    id = models.TextField(
        _("PayloadUniqueID"),
        primary_key=True,
        default=uuid_generator
    )

    owner = models.ForeignKey(
        UserBase,
        on_delete=models.CASCADE
    )

    audio_file_name = models.TextField(
        _("FileName"),
        max_length=128,
        blank=False
    )

    uploaded_at = models.DateTimeField(
        _("UploadedAt"),
        default=timezone.now
    )

    status = models.SmallIntegerField(
        _("Status"),
        choices=PayloadStatus.choices,
        default=PayloadStatus.UNKNOWN
    )

    message = models.CharField(
        _("Message"),
        blank=True,
        max_length=256
    )

    transcribe = models.CharField(
        _("Transcribe"),
        blank=True,
        max_length=2048
    )

    response: PayloadResponse()
