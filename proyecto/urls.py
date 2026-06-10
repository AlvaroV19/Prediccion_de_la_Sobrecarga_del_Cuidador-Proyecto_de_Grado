from django.contrib import admin
from django.urls import path
from .views import main, predict

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='home'),
    path('main/', main, name='main'),
    path('prediccion/', predict, name='prediccion'),
]
