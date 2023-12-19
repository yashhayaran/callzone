from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from playground.forms import AudioFileUploadForm, ContentTypeRestrictedFileField


@login_required()
def upload_file(request):
    """
    USER uploaded a client validated audio file to server via api
    '/playground/upload_file/'

    Create dummy AudioFileUploadForm object with input files to re-validate again by server again by use of
    AudioFileUploadForm class.

    """
    try:
        is_valid = False
        error: str = ""
        if request.method == 'POST':
            user_id = request.user.id
            form = AudioFileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data.get('audio_file')
                if file is not None and user_id is not None:
            else:
                error: list = form.errors
                print(error.pop())

        if is_valid:
            file_handler.handle_file(file, user_id)
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
