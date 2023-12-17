from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from playground.forms import AudioFileUploadForm, ContentTypeRestrictedFileField
from playground.modules.file_handler import handle_file


@login_required()
def upload_file(request):
    """
    We expect an audio file being uploaded by user.
    Audio file being validated.
    If passes:
        - Handles the audio file to Handler
    Else:
        - Returns an error log to user
    """
    try:
        error: str = ""
        # Uses this form as a placeholder
        form = AudioFileUploadForm()
        if request.method == 'POST':
            user_id = request.user.id
            file_submitted = True
            # Try to validate the form here
            form = AudioFileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data.get('audio_file')
                if file is not None and user_id is not None:
                    handle_file(file, user_id)
            else:
                error: list = form.errors
                print(error.pop())

    except Exception as ex:
        error = str(ex)

    response = {
        "results": {
            "file-uploaded": True
        },
        "errors": [
            error
        ]
    }
    return JsonResponse(data=response)
