from django.conf.urls import *  # NOQA
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
from cms.sitemaps import CMSSitemap
from accounts.forms import SignupFormExtra

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^database/$', 'BIDP.plugins.upload.cms_plugins.process_operation', name = "process_operation"),
)

urlpatterns += i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),  # NOQA
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^my-profile/$', 'accounts.views.redirct_profile'),
    url(r'^my-profile/(?P<username>(?!signout|signup|signin)[\@\.\w-]+)/$', 'userena.views.profile_detail', name = 'profile_detail'),
    url(r'^accounts/sign/$', 'accounts.views.sign', name = "sign"),
    url(r'^accounts/signup/$', 'userena.views.signup', {'signup_form': SignupFormExtra}),
    url(r'^accounts/', include('userena.urls')),
    url(r'^', include('cms.urls')),
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',  # NOQA
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ) + staticfiles_urlpatterns() + urlpatterns  # NOQA
