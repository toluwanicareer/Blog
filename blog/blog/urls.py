from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


    

urlpatterns = [
    # django admin
    path('admin/', admin.site.urls),

    # User management
    path('accounts/', include('django.contrib.auth.urls')), 

    # local apps
    path('', include('homeblog.urls')),

    # 3rd party apps
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
