from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'server.views.loginform', name='home'),
    url(r'^loginform$', 'server.views.loginform', name='loginform'),
    url(r'^login$', 'server.views.login', name='login'),
    url(r'^logout$', 'server.views.logout', name='logout'),
    url(r'^xrds$', 'server.views.xrds', name='xrds'),
    url(r'^openid$', 'server.views.openid', name='openid'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
