from django.shortcuts import render_to_response
from vexim.controlpanel import models
from vexim.controlpanel import authz
from vexim.controlpanel import common

def login(request):
    m = User.objects.get(username=request.POST['username'])
    if m.password == request.POST['password']:
        request.session['member_id'] = m.id
        return HttpResponse("You're logged in.")
    else:
        return HttpResponse("Your username and password didn't match.")


def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")


def check_auth(request):
    # TODO(avleen): Ensure user is actually logged in
    return True
