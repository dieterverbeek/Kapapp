# kapperapp/urls.py (YOUR PROJECT'S MAIN URLS.PY)

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static # For MEDIA_URL

# NEW IMPORT for static files from STATICFILES_DIRS
from django.contrib.staticfiles.urls import staticfiles_urlpatterns




# Import specific views explicitly
from kapperapp.views import (
    login_view, logout_view, dashboard_view, klanten_view,
    afrekenen_view, klant_toevoegen_view, klant_verwijderen_view, klant_bewerken_view, export_klanten_excel
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('klanten/', klanten_view, name='klanten'),
    path('afrekenen/', afrekenen_view, name='afrekenen'),
    path('klant_toevoegen', klant_toevoegen_view, name='klant_toevoegen'),
    path('klant_verwijderen/<int:klant_id>/', klant_verwijderen_view, name='klant_verwijderen'),
    path('klanten/bewerk/<int:klant_id>/', klant_bewerken_view, name='klant_bewerken'),
    path('export/excel/', export_klanten_excel, name='export_klanten_excel'),
]

# VERY IMPORTANT: Serve static and media files in development
if settings.DEBUG:
    # This adds URL patterns to serve static files from STATICFILES_DIRS and app static folders
    urlpatterns += staticfiles_urlpatterns()
    # This adds URL patterns to serve media files (user uploads)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)