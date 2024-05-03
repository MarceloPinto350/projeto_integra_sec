from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView

# imports para uso dos modelos e templates criados
#from django.template import loader
#from django.http import Http404

from .models import Categoria, Abrangencia, AreaNegocial, Sistema


def custom_login(request, **kwargs):
    if request.user.is_authenticated:
        return redirect('index')
    return LoginView.as_view(template_name='bibpub/template/login.html')(request, **kwargs)
 
@login_required()
def index(request):
    return render(request, 'sysdso/index.html')