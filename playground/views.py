from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import ValidationError
from django.shortcuts import render

from .forms import AudioFileUploadForm
from .modules.file_handler import handle_file


@login_required(login_url='/login')
def playground_main(request):
    """Method to render the main page view to user
    """
    form = AudioFileUploadForm()
    return render(
        request, 'playground/playground.html',
        {
            'form': form,
            'file_uploaded': False
        }
    )


@login_required(login_url='/login')
def upload_file(request):
    file_uploaded = False
    upload_status = False
    error = ''
    form = AudioFileUploadForm()

    try:
        if request.method == 'POST':
            user_id = request.user.id
            file_submitted = True
            # Try to validate the form here
            form = AudioFileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data.get('audio_file')
                if file is not None and user_id is not None:
                    handle_file(file, user_id)


    except ValidationError as ve:
        x = ve
        y = ve
    except Exception as ex:
        x = ex
        y = ex

    finally:
        return render(
            request, 'playground/playground.html',
            {
                'form': form,
                'file_submitted': file_submitted,
                'upload_success': upload_status,
                'error_message': error
            }
        )
