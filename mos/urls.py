import django.views.i18n
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

import web.views
from cal.feeds import EventFeed

admin.autodiscover()

urlpatterns = [
    path('admin/jsi18n/', django.views.i18n.JavaScriptCatalog.as_view()),
    path('admin/', admin.site.urls),


    path('feeds/events/', EventFeed()),

    path('calendar/', include('cal.urls')),
    path('project/', include('projects.urls')),
    path('member/', include('members.urls')),
    path('announce/', include('announce.urls')),
    path('things/', include('things.urls')),
    path('cellardoor/', web.views.display_cellardoor),
    path('spaceapi.json', web.views.spaceapi),
    path('', web.views.display_main_page),
    path('mos', web.views.display_main_page),
]

urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
