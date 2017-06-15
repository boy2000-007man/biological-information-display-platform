from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

# Create your views here.
from .forms import SigninForm, SignupFormExtra

def sign(request):
    signin_form = SigninForm()
    signup_form = SignupFormExtra()
    return render(
        request,
        "sign_form.html",
        {
            "signin_form": signin_form,
            "signup_form": signup_form
        }
    )

def redirct_profile(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('accounts.views.redirct_profile') + request.user.username + "/")
    return HttpResponseRedirect("/")
