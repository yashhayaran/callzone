import copy

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from playground.forms import AudioFileUploadForm, ContentTypeRestrictedFileField
from playground.modules.payload_manager import PayloadManager
from playground.modules.upload_reponse import UploadResponse

__manager = PayloadManager()


@login_required()
def upload_file(request):
    """
    USER uploaded a client validated audio file to server via api
    '/playground/upload_file/'

    Create dummy AudioFileUploadForm object with input files to re-validate again by server again by use of
    AudioFileUploadForm class.

    """
    current_user = None
    audio_file = None
    is_valid_file = False
    response_json = UploadResponse()
    try:
        if request.method == 'POST':
            current_user = copy.deepcopy(request.user)
            form = AudioFileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                audio_file = form.cleaned_data.get('audio_file')
                if audio_file is not None:
                    if current_user is not None:
                        is_valid_file = True
                    else:
                        response_json.errors_list.append("User is invalid to perform this action")
                else:
                    response_json.errors_list.append("Uploaded file is invalid or upload failure has occurred")
            else:
                response_json.errors_list.append(form.errors)

        if is_valid_file:
            __manager.add_payload(
                current_user,
                audio_file,
                response_json
            )

    except Exception as ex:
        response_json.errors_list.append(str(ex))

    finally:
        response = {
            "results": {
                "file-uploaded": True
            },
            "errors": [
                error
            ]
        }
        return JsonResponse(data=response_json)
