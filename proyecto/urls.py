from django.contrib import admin
from django.urls import path
from .views import login_screen, main, predict

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_screen, name='login'),
    path('', login_screen, name='home'),
    path('main/', main, name='main'),
    path('prediccion/', predict, name='prediccion'),
]
