from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import redirect, render_to_response
from vexim.controlpanel import common
from vexim.controlpanel.models import Domain

import hashlib
import os
import sys
import types


@login_required
def index(request, domain_letter=None):
    if not request.user.is_authenticated():
        return redirect('/accounts/login/')
    if not request.user.has_perm('controlpanel.siteadmin'):
        return redirect('/accounts/login/')

    reply_dict = common.get_reply_dict(request)
    reply_dict['local_domains'] = Domain.objects.filter(type='local')
    reply_dict['alias_domains'] = Domain.objects.filter(type='alias')
    reply_dict['relay_domains'] = Domain.objects.filter(type='relay')

    return render_to_response('controlpanel/siteadmin_index.html', reply_dict,
                              context_instance=RequestContext(request))


@login_required
def addalias(request):
    if not request.user.has_perm('controlpanel.siteadmin'):
        return redirect('/accounts/login/')

    reply_dict = common.get_reply_dict(request)

    if request.method == 'GET':
        return render_to_response('controlpanel/siteadmin_addalias.html',
                reply_dict, context_instance=RequestContext(request))

    elif request.method == 'POST':
        if not request.POST.has_key('aliasdomain'):
            msg = 'Error: You must specify an alias domain name'
            msgclass = 'error'
            return render_to_response('controlpanel/siteadmin_addalias.html',
                    reply_dict, context_instance=RequestContext(request))
        elif not request.POST.has_key('targetdomain'):
            msg = 'Error: You must specify a domain name to alias to'
            msgclass = 'error'
            return render_to_response('controlpanel/siteadmin_addalias.html',
                    reply_dict, context_instance=RequestContext(request))

        aliasdomain = request.POST['aliasdomain']
        targetdomain = request.POST['targetdomain']
        if Domain.objects.filter(domain=aliasdomain):
            msgclass = 'error'
            msg = 'Domain %s is already present in the system' % aliasdomain
        else:
            try:
                d = Domain(domain=aliasdomain,
                           maildir=targetdomain,
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
        else:
            return render_to_response('controlpanel/siteadmin_addalias.html',
                    reply_dict, context_instance=RequestContext(request))



@login_required
def addrelay(request):
    if not request.user.has_perm('controlpanel.siteadmin'):
        return redirect('/accounts/login/')

    reply_dict = common.get_reply_dict(request)

    if request.method == 'POST':
        relaydomain = request.POST['relaydomain']
        if Domain.objects.filter(domain=relaydomain):
            msgclass = 'error'
            msg = 'Domain %s is already present in the system' % relaydomain
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
    if not request.user.has_perm('controlpanel.siteadmin'):
        return redirect('/accounts/login/')

    reply_dict = common.get_reply_dict(request)
    if request.method == 'POST':
        # We mostly check for errors, make this the default msgclass to return.
        # If things go well, we can change it to 'ok' later :-)
        msgclass = 'error'
        if len(request.POST['localdomain']) == 0:
            msg = 'Error: Please enter a valid domain name'
        elif request.POST['password_one'] != request.POST['password_two']:
            msg = 'Error: Passwords do not match'
        elif len(request.POST['password_one']) == 0 or \
                len(request.POST['password_two']) == 0:
            msg = 'Error: Passwords cannot be blank'
        elif not request.POST['uid'].isdigit():
            msg = 'Error: UID must be numeric'
        elif not request.POST['gid'].isdigit():
            msg = 'Error: GID must be numeric'
        elif not request.POST['sa_tag'].isdigit():
            msg = 'Error: Spam tag score must be numeric'
        elif not request.POST['sa_refuse'].isdigit():
            msg = 'Error: Spam refuse score must be numeric'
        elif not request.POST['max_accounts'].isdigit():
            msg = 'Error: Maximum number of accounts must be numeric'
        elif common.check_domain_exists(request.POST['localdomain']):
            msg = 'Error: Domain already exists'
        else:
            avscan = 1 if request.POST.has_key('avscan') else 0
            blocklists = 1 if request.POST.has_key('blocklists') else 0
            complexpass = 1 if request.POST.has_key('complexpass') else 0
            mailinglists = 1 if request.POST.has_key('mailinglists') else 0
            pipe = 1 if request.POST.has_key('pipe') else 0
            spamassassin = 1 if request.POST.has_key('spamassassin') else 0
            try:
                domain = Domain(domain=request.POST['localdomain'],
                                type='local',
                                enabled=True,
                                maildir=os.path.join(settings.VEXIM_MAILHOME,
                                                     request.POST['localdomain']),
                                uid=request.POST['uid'],
                                gid=request.POST['gid'],
                                max_accounts=request.POST['max_accounts'],
                                avscan=avscan,
                                blocklists=blocklists,
                                complexpass=complexpass,
                                mailinglists=mailinglists,
                                pipe=pipe,
                                spamassassin=spamassassin,
                                sa_tag=request.POST['sa_tag'],
                                sa_refuse=request.POST['sa_refuse'],
                                tagline=request.POST['tagline'])
                domain.save()
                # Django has an annoying limitation: The username is limited to
                # 30 chars. Whose bright idea was that?
                # Doesn't matter. We use the email field for user authentication
                # anyway, so let's make the username the first 30 chars of the
                # md5, just to keep it random
                user = User.objects.create_user(username=hashlib.md5('postmaster@%s' % request.POST['localdomain']).hexdigest(),
                                                email='postmaster@%s' % request.POST['localdomain'],
                                                password=request.POST['password_one'])
                user.save()
                user.userprofile_set.create(domain_id=domain.id,
                                            localpart='postmaster',
                                            uid=domain.uid,
                                            gid=domain.gid,
                                            maildir=os.path.join(domain.maildir,
                                                                 'postmaster'),
                                            type='admin',
                                            antivirus_enabled=domain.avscan,
                                            spamassassin_enabled=domain.spamassassin,
                                            sa_tag=domain.sa_tag,
                                            sa_refuse=domain.sa_refuse)
                msg = 'Domain %s added' % domain.domain
                msgclass = 'ok'
            except:
                msg = 'Error: Unable to create local domain: %s' % sys.exc_info()[1]

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
