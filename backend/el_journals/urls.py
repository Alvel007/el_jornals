from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from .views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', logout_view, name='logout'),
    path('staff/', include('staff.urls')),
    path('op_journal/', include('op_journal.urls')),
    path('login/', login_view, name='login'),
    path('', RedirectView.as_view(url='op_journal/')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
