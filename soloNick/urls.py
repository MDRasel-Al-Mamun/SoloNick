from django.contrib import admin
from django.conf import settings
from filebrowser.sites import site
from django.conf.urls.static import static
from django.urls import path, re_path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^admin/filebrowser/', site.urls),
    re_path(r'^tinymce/', include('tinymce.urls')),

    path('', include('home.urls')),
    path('blog/', include('blog.urls')),
    path('user/', include('user.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('my_profile/', include('myProfile.urls')),
    path('authentication/', include('authentication.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
