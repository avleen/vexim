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
    d = {'realname': realname,
         'emailaddress': emailaddress,
         'quota': quota}
    return d

def get_quota(username):
    # TODO(avleen): Implement quota checks
    if not username:
        return 'Unknown'
    else:
        return 'foo'
