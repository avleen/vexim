from django.conf import settings
from vexim.controlpanel.models import Domain

def check_domain_exists(domain):
    d = Domain.objects.filter(domain=domain)
    if d.count() > 0:
        return True
    else:
        return False


def get_reply_dict(request):
    realname = None
    emailaddress = None
    username = None
    if request.session.has_key('realname'):
        realname = request.session['realname']
    if request.session.has_key('emailaddress'):
        emailaddress = request.session['emailaddress']
    if request.session.has_key('username'):
        username = request.session['username']
    quota = get_quota(username)
    settings_dict = {'uid': settings.VEXIM_UID,
                     'gid': settings.VEXIM_GID,
                     'sa_tag': settings.VEXIM_SA_TAG,
                     'sa_refuse': settings.VEXIM_SA_REFUSE,
                     'mailhome': settings.VEXIM_MAILHOME}
    d = {'realname': realname,
         'emailaddress': emailaddress,
         'quota': quota,
         'settings': settings_dict}
    return d


def get_quota(username):
    # TODO(avleen): Implement quota checks
    if not username:
        return False
    else:
        return 'foo'
