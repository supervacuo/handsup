from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


from core.views import (HomeView, CampaignAddView, CampaignDetailView,
                        HeroRegisterView, HeroDetailView, CampaignJoinView,
                        CampaignOwnView)


urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),

    url(r'^campaign/add/', CampaignAddView.as_view(), name='campaign_add'),

    url(r'^campaign/(?P<slug>[-_\w]+)/join/$', CampaignJoinView.as_view(), name='campaign_join'),
    url(r'^campaign/(?P<slug>[-_\w]+)/own/$', CampaignOwnView.as_view(), name='campaign_own'),
    url(r'^campaign/(?P<slug>[-_\w]+)/$', CampaignDetailView.as_view(), name='campaign_detail'),

    url(r'^user/(?P<username>[-_\w]+)/$', HeroDetailView.as_view(), name='hero_detail'),
    url(r'^register/', HeroRegisterView.as_view(), name='user_register'),
    url(r'^login/', 'django.contrib.auth.views.login', name='user_login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {
        'next_page': '/'
    }, name='user_logout'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
    )

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
