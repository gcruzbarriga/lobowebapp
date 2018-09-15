from django.conf.urls import url, include
from django.contrib import admin
from control import views

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^comida/$', views.comida, name="comida"),
    url(r'^confirmar/$', views.confirmacion, name="confirmacion"),
    url(r'^confirmarComida/$', views.confirmacionComida, name="confirmacionComida"),
    url(r'^reporte/$', views.reporte, name="reporte"),
    url(r'^export/csv/', views.export_users_csv, name="export_users_csv"),
    
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^admin/', admin.site.urls),
]
