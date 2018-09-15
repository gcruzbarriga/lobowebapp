from django.conf.urls import url, include
from django.contrib import admin
from control import views

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url('comida', views.comida, name="comida"),
    url('confirmar', views.confirmacion, name="confirmacion"),
    url('confirmarComida', views.confirmacionComida, name="confirmacionComida"),
    url('reporte', views.reporte, name="reporte"),
    url('export/csv/', views.export_users_csv, name="export_users_csv"),
    
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^admin/', admin.site.urls),
]
