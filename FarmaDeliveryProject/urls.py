from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from core.auth_views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login/logout personalizados
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # URLs de auth de Django
    path('accounts/', include('django.contrib.auth.urls')),

    # Rutas de la app core
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)