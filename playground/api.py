import copy

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.http import JsonResponse
from django.shortcuts import render

from main.models import UserBase
from playground.forms import AudioFileUploadForm, ContentTypeRestrictedFileField
from playground.models import PayloadStatus, PayloadResponse
from playground.modules.context_manager import ContextManager

__manager = ContextManager()


@login_required()
def upload_file(request):
    """
    USER uploaded a client validated audio file to server via api
    '/playground/upload_file/'

    Create dummy AudioFileUploadForm object with input files to re-validate again by server again by use of
    AudioFileUploadForm class.

    """
    current_user: UserBase
    audio_file: UploadedFile
    payload_res = PayloadResponse(
        "NA"
    )
    try:
        if request.method == 'POST':
            # current_user = copy.deepcopy(request.user)
            current_user = request.user
            form = AudioFileUploadForm(request.POST, request.FILES)
            try:
                if form.is_valid():
                    audio_file = form.cleaned_data.get('audio_file')
                    if audio_file is not None:
                        if current_user is not None:
                            payload_res.status = PayloadStatus.UPLOADED
                        else:
                            payload_res.status = PayloadStatus.ERROR
                            payload_res.errors_list.append("User is invalid to perform this action")
                    else:
                        payload_res.status = PayloadStatus.ERROR
                        payload_res.errors_list.append("Uploaded file is invalid or upload failure has occurred")
                else:
                    payload_res.status = PayloadStatus.ERROR
                    payload_res.errors_list.append(form.errors)
            except ValidationError as ve:
                payload_res.status = PayloadStatus.ERROR
                payload_res.errors_list.append(ve.message)

        if payload_res.status is PayloadStatus.UPLOADED:
            __manager.try_add_payload(current_user,
                                      audio_file,
                                      payload_res
                                      )

    except Exception as ex:
        payload_res.errors_list.append(str(ex))

    finally:
        return JsonResponse(data=payload_res)


@login_required()
def fetch_user_payloads(request):
    """
    API to return collection of PayloadRequestResponse of current user
    Client fetch the data for current logged-in user
        -
    """
    response_json: PayloadResponse = PayloadResponse(
        None
    )
    infos = None
    try:
        if request.method == 'POST':
            info_collection: list = None
            current_user: UserBase = request.user
            infos = __manager.get_user_payloads(current_user,
                                                info_collection)

    except Exception as ex:
        response_json.errors_list.append(str(ex))

    finally:
        print(infos)
        return JsonResponse(data=str(response_json))
