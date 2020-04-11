"""afkforum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
# dette under legges også inn for å kunne laste opp bildefiler
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(url='forumApp/')),
    path('forumapp/', RedirectView.as_view(url='forumApp/')),
    path('forumApp/', include('forumApp.urls')),
    path('admin/', admin.site.urls),
]


# kan hende dette skal i urls.py som ligger inni forumApp-mappen
# er lagt inn i for å kunne laste opp bildefiler
# Det den gjør: hvis settings er i DEBUG-modus (noe som den er når vi utvikler) legger
# vi til et spesielt view som serves media-url-ene. Bare for utviling
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)