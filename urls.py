from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^vexim/', include('vexim3.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^$', 'controlpanel.authz.login'),
    (r'^accounts/login/$', 'controlpanel.authz.login'),
    (r'^logout/$', 'controlpanel.authz.logout'),
    (r'^update/password/$', 'controlpanel.update.password'),
    (r'^update/forwarding/$', 'controlpanel.update.forwarding'),
    (r'^update/maxmsgsize/$', 'controlpanel.update.maxmsgsize'),
    (r'^update/vacation/$', 'controlpanel.update.vacation'),
    (r'siteadmin/$', 'controlpanel.siteadmin.index'),
    (r'siteadmin/domains/(?P<domain_letter>\w)/$', 'controlpanel.siteadmin.index'),
    (r'siteadmin/addalias/$', 'controlpanel.siteadmin.addalias'),
    (r'siteadmin/addlocal/$', 'controlpanel.siteadmin.addlocal'),
    (r'siteadmin/addrelay/$', 'controlpanel.siteadmin.addrelay'),
)
