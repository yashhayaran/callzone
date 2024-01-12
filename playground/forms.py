from django import forms
from django.template.defaultfilters import filesizeformat

from .models import PayloadStatus


class ContentTypeRestrictedFileField(forms.FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    error_message: str = None
    status: PayloadStatus = PayloadStatus.UNKNOWN

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

        # mark the status as success
        self.status = PayloadStatus.UPLOADED

        if data.content_type in self.content_types:
            if data.size > self.max_upload_size:
                self.error_message = (f'Please keep file-size under {filesizeformat(self.max_upload_size)}. Current '
                                      f'file-size {filesizeformat(data.size)}')
        else:
            self.error_message = 'File format is invalid, only MPEG-3 (.mp3) is supported.'

        if self.error_message is not None:
            raise forms.ValidationError(f"{self.error_message}")

        return data


class AudioFileUploadForm(forms.Form):
    audio_file = ContentTypeRestrictedFileField(
        content_types=['audio/mpeg'],
        max_upload_size=5242880,
        label='audio_file',
        widget=forms.FileInput(attrs={'accept': 'audio/aac,audio/mpeg,audio/wav,audio/webm,audio/x-flac,audio/flac'})
    )

    class Meta:
        fields = 'audio_file'
