from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import redirect, render_to_response
from vexim.controlpanel import authz
from vexim.controlpanel import common
from vexim.controlpanel.models import Domain

import sys


def index(request, domain_letter=None):
    print request.user.is_authenticated()
    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    # If the current user isn't the siteadmin, redirect them away
    if request.user.username != settings.VEXIM_ADMIN_USER:
        print request.user.username
        return redirect('/accounts/login/')

    reply_dict = common.get_reply_dict(request)
    domains = Domain.objects.all()

    return render_to_response('controlpanel/siteadmin_index.html', reply_dict,
                              context_instance=RequestContext(request))


@login_required
def addalias(request):
    # If the current user isn't the siteadmin, redirect them away
    if request.user.username != settings.VEXIM_ADMIN_USER:
        return redirect('/accounts/login/')

    reply_dict = common.get_reply_dict(request)

    if request.POST.has_key('aliasdomain'):
        aliasdomain = request.POST['aliasdomain']
        targetdomain = request.POST['targetdomain']
        if Domain.objects.filter(domain=aliasdomain):
            msgclass = 'error'
            msg = 'Domain %s is already present in the system' % aliasdomain
        else:
            try:
                d = Domain(domain=request.POST['aliasdomain'],
                           maildir=request.POST['targetdomain'],
                           type='alias',
                           enabled=True)
                d.save()
                msgclass = 'ok'
                msg = 'Alias domain %s directed to %s' % (aliasdomain, targetdomain)
            except:
                msgclass = 'error'
                msg = 'Error: Unable to create alias domain: %s' % sys.exc_info()[1]
        reply_dict['aliasdomain'] = aliasdomain
        reply_dict['targetdomain'] = targetdomain
        reply_dict['msg'] = msg
        reply_dict['msgclass'] = msgclass

        if msgclass == 'ok':
            return render_to_response('controlpanel/siteadmin_index.html',
                    reply_dict, context_instance=RequestContext(request))

    return render_to_response('controlpanel/siteadmin_addalias.html',
            reply_dict, context_instance=RequestContext(request))


@login_required
def addrelay(request):
    # If the current user isn't the siteadmin, redirect them away
    if request.user.username != settings.VEXIM_ADMIN_USER:
        return redirect('/accounts/login/')

    reply_dict = common.get_reply_dict(request)

    if request.POST.has_key('relaydomain'):
        relaydomain = request.POST['relaydomain']
        if Domain.objects.filter(domain=relaydomain):
            msgclass = 'error'
            msg = 'Domain %s is already present in the system' % aliasdomain
        else:
            try:
                d = Domain(domain=request.POST['relaydomain'],
                           type='relay',
                           enabled=True)
                d.save()
                msgclass = 'ok'
                msg = 'Relay domain %s created' % relaydomain
            except:
                msgclass = 'error'
                msg = 'Error: Unable to create relay domain:' % sys.exc_info()[1]
        reply_dict['relaydomain'] = relaydomain
        reply_dict['msg'] = msg
        reply_dict['msgclass'] = msgclass
        return render_to_response('controlpanel/siteadmin_index.html',
                reply_dict, context_instance=RequestContext(request))

    return render_to_response('controlpanel/siteadmin_addrelay.html',
            reply_dict, context_instance=RequestContext(request))


@login_required
def addlocal(request):
    # If the current user isn't the siteadmin, redirect them away
    if request.user.username != settings.VEXIM_ADMIN_USER:
        return redirect('/accounts/login/')

    reply_dict = common.get_reply_dict(request)

    if request.POST.has_key('localdomain'):
        if len(request.POST['localdomain']) == 0:
            msg = 'Error: Please enter a valid domain name'
            msgclass = 'error'
        elif request.POST['password_one'] != request.POST['password_two']:
            msg = 'Error: Passwords do not match'
            msgclass = 'error'
        elif len(request.POST['password_one']) == 0 or \
                len(request.POST['password_two']) == 0:
            msg = 'Error: Passwords cannot be blank'
            msgclass = 'error'
        elif not request.POST['uid'].isdigit():
            msg = 'Error: UID must be numeric'
            msgclass = 'error'
        elif not request.POST['gid'].isdigit():
            msg = 'Error: GID must be numeric'
            msgclass = 'error'
        elif not request.POST['sa_tag'].isdigit():
            msg = 'Error: Spam tag score must be numeric'
            msgclass = 'error'
        elif not request.POST['sa_refuse'].isdigit():
            msg = 'Error: Spam refuse score must be numeric'
            msgclass = 'error'
        else:
            try:
                # TODO(avleen): Create the local domain
                d = Domain(domain=request.POST['relaydomain'],
                           type='relay',
                           enabled=True)
                d.save()
                msg = 'Domain %s added' % request.POST['localdomain']
                msgclass = 'ok'
            except:
                msg = 'Error: Unable to create local domain'
                msgclass = 'error'

        # This is a hack - we can take the variables we care about, and put them
        # back into reply_dict and send them back to the form. This lets us
        # re-populate the form on load if we failed to add the domain.
        # We can't just:  reply_dict.update(request.POST)
        # If we do that, our variables get printed as:  u['example.com']
        posted = ('localdomain', 'uid', 'gid', 'maxaccounts',
                  'piping_enabled', 'antivirus_enabled', 'antivirus_enabled',
                  'spamassassin_enabled', 'sa_tag', 'sa_refuse')
        for var in posted:
            if request.POST.has_key(var):
                reply_dict.update({var: request.POST[var]})
        reply_dict['msg'] = msg
        reply_dict['msgclass'] = msgclass
        if msgclass == 'ok':
            return render_to_response('controlpanel/siteadmin_index.html',
                    reply_dict, context_instance=RequestContext(request))

    # If we return this, it is because this is the first page load or
    # msgclass=="error"
    return render_to_response('controlpanel/siteadmin_addlocal.html',
            reply_dict, context_instance=RequestContext(request))
