"""
Definition of urls for cbtv02.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from django.conf.urls.static import static
import app.forms
import app.views
from cbtv02 import settings
# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^register', app.views.register, name='register'),
    url(r'^boardpage', app.views.boardpage, name='boardpage'),
    url(r'^result', app.views.result, name='result'),
    url(r'^reset', app.views.reset, name='reset'),
    #url(r'^questionpage/(?P<module>\w+)', app.views.questionpage, name='questionpage'),
    url(r'^questionpage', app.views.questionpage, name='questionpage'),
    url(r'^postanswer', app.views.postanswer, name='postanswer'),
    url(r'^get_answer', app.views.get_answer, name='get_answer'),
    #url(r'^login/$',
    #    django.contrib.auth.views.login,
    #    {
    #        'template_name': 'app/login.html',
    #        'authentication_form': app.forms.BootstrapAuthenticationForm,
    #        'extra_context':
    #        {
    #            'title': 'Log in',
    #            'year': datetime.now().year,
    #        }
    #    },
    #    name='login'),
    url(r'^login/$',app.views.mylogin,name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls),name='adminlink'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)