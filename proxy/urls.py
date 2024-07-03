from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

import proxy.views as views

urlpatterns = [
    path('thredds/wms/<path:request_path>', views.proxy_wms_request, name='proxy_wms_request'),
    path('home', views.home, name='home'),
    path('', views.home, name='home')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)