from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import ValidationError
from django.shortcuts import render

from .forms import AudioFileUploadForm


@login_required(login_url='/login')
def playground_main(request):
    """
    Method to render the main page view to user
    """
    return render(
        request, 'playground/playground.html'
    )
