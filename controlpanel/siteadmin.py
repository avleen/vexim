from django.template import RequestContext
from django.shortcuts import render_to_response
from vexim.controlpanel import authz
from vexim.controlpanel import common
from vexim.controlpanel.models import Domain


def index(request, domain_letter=None):
    reply_dict = common.get_reply_dict(request)
    if not authz.check_auth(request):
        # TODO(avleen): Return the login page
        return render_to_response('controlpanel/login.html')

    domains = Domain.objects.all()

    return render_to_response('controlpanel/siteadmin_index.html', reply_dict,
                              context_instance=RequestContext(request))


def addalias(request):
    reply_dict = common.get_reply_dict(request)
    if not authz.check_auth(request):
        # TODO(avleen): Return the login page
        return render_to_response('controlpanel/login.html')

    if request.POST.has_key('aliasdomain'):
        aliasdomain = request.POST['aliasdomain']
        targetdomain = request.POST['targetdomain']
        try:
            # TODO(avleen): Create the alias domain
            msgclass = 'ok'
            msg = 'Alias domain %s directed to %s' % (aliasdomain, targetdomain)
        except:
            msgclass = 'error'
            msg = 'Error: Unable to create alias domain'
        reply_dict['msg'] = msg
        reply_dict['msgclass'] = msgclass

    return render_to_response('controlpanel/siteadmin_addalias.html',
            reply_dict, context_instance=RequestContext(request))
