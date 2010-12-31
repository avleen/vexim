from django.shortcuts import render_to_response
from vexim.controlpanel import models
from vexim.controlpanel import authz
from vexim.controlpanel import common


def index(request):
    reply_dict = common.get_reply_dict(request)
    if not authz.check_auth(request):
        # TODO(avleen): Return the login page
        return render_to_response('controlpanel/login.html')

    # TODO(avleen): If the users is a siteadmin, return the siteadmin page.
    # TODO(avleen): If the users is a domainadmin, return the domainadmin page.
    return render_to_response('controlpanel/user_index.html', reply_dict)
