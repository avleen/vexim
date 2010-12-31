from django.shortcuts import render_to_response
from vexim.controlpanel import models
from vexim.controlpanel import authz
from vexim.controlpanel import common

def forwarding(request):
    # TODO(avleen): Update forwarding
    return

def maxmsgsize(request):
    # TODO(avleen): Update maxmsgsize
    return

def password(request):
    reply_dict = common.get_reply_dict(request)
    if not authz.check_auth(request):
        # TODO(avleen): Return the login page
        return render_to_response('controlpanel/login.html')

    password_one = request.POST['password_one']
    password_two = request.POST['password_two']
    if len(password_one) > 0 and (password_one == password_two):
        # TODO(avleen): Reset the password in the db
        msgclass = 'ok'
        msg = "Your password has been updated."
    elif len(password_one) == 0:
        msgclass = 'error'
        msg = "Passwords cannot be blank."
    elif password_one != password_two:
        msgclass = 'error'
        msg = "Passwords do not match."
    else:
        msgclass = 'error'
        msg = "Unknown error."

    reply_dict['msgclass'] = msgclass
    reply_dict['msg'] = msg

    return render_to_response('controlpanel/user_index.html', reply_dict)

def vacation(request):
    # TODO(avleen): Update vacation
    return
