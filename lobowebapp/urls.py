"""lobowebapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from control import views

urlpatterns = [
    url('', views.index, name="home"),
    # path('comida', views.comida.as_view(), name="comida"),
    # path('confirmar', views.confirmacion.as_view(), name="confirmacion"),
    # path('confirmarComida', views.confirmacionComida.as_view(), name="confirmacionComida"),
    # path('reporte', views.reporte.as_view(), name="reporte"),
    # path('export/csv/', views.export_users_csv.as_view(), name="export_users_csv"),
    
    # path('accounts/', include('registration.backends.default.urls')),
    # path('admin/', admin.site.urls),
    url(r'^admin/', admin.site.urls),
]
