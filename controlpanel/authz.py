from django.conf import settings
from django.contrib import auth
from django.contrib.auth import login, authenticate 
from django.contrib.auth.models import User
from django.http import Http404
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect, render_to_response
from vexim.controlpanel import models
from vexim.controlpanel import common

class VeximAuth:
    def authenticate(self, username=None, password=None):
        if username == settings.VEXIM_ADMIN_USER:
            # Authenticate the site admin
            if password == settings.VEXIM_ADMIN_PASS:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User(username=username, password='unused')
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
                return user
            return None
        else:
            try:
                user = User.objects.get(email=username, password=password)
            except User.DoesNotExist:
                return None
            else:
                return user

    def get_user(self, user_id):
        try:
            return User.objects.get(email=user_id)
        except User.DoesNotExist:
            return None


def login(request):
    # If the users it not currently logged in, log them in.
    # Then redirect the user to the right place.
    if not request.user.is_authenticated():
        # Was this a GET or a POST?
        # GET == generate login page
        # POST = process login
        if request.method == 'GET':
            return render_to_response('registration/login.html', {},
                                      context_instance=RequestContext(request))
        elif request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            if not username or not password:
                return redirect('/accounts/login/')
            user = authenticate(username=username, password=password)
            if not user:
                return redirect('/accounts/login/')
            else:
                auth.login(request, user)
        else:
            raise Http404

    # This block is executed for logged in users
    if user.has_perm('controlpanel.monkeyarse'):
        print request.user.is_authenticated()
        return redirect('/siteadmin/')
    elif user.has_perm('domainadmin'):
        return redirect('/domainadmin/')
    else:
        return redirect('/user/')


def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")
