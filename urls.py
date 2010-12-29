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
    (r'^$', 'controlpanel.views.index'),
    (r'^login/$', 'controlpanel.authz.login'),
    (r'^logout/$', 'controlpanel.authz.logout'),
    (r'^update/password/$', 'controlpanel.update_profile.password'),
    (r'^update/forwarding/$', 'controlpanel.update_profile.forwarding'),
    (r'^update/maxmsgsize/$', 'controlpanel.update_profile.maxmsgsize'),
    (r'^update/vacation/$', 'controlpanel.update_profile.vacation'),
)
