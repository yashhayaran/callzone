from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from common.models import uuid_generator
from main.models import UserBase

from django.utils.translation import gettext_lazy as _


class PayloadStatus(models.IntegerChoices):
    SUCCESS_TRANSCRIBE = 1
    SUCCESS_UPLOAD = 2
    ERROR_UPLOAD_SERVER = 3
    ERROR_INVALID_FILE_FORMAT = 4
    ERROR_MAX_SIZE_REACHED = 5
    ERROR_UNABLE_PROCESS = 6
    ERROR_UNKNOWN = 7
    FAIL_NO_TRANSCRIBE = 8


class PayloadInfo(models.Model):
    """
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
        to=UserBase,
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

    status = models.IntegerField(
        _("StatusCode"),
        choices=PayloadStatus.choices,
        default=PayloadStatus.ERROR_UNKNOWN
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
