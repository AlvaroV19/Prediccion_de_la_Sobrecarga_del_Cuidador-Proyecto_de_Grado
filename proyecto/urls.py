from django.contrib import admin
from django.urls import path
from .views import (
    login_screen, 
    main, predict, 
    statistics, 
    register_screen, 
    forgot_password_screen,
    reset_password_screen,
    pending_reset_screen
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_screen, name='login'),
    path('', login_screen, name='home'),
    path('registro/', register_screen, name='registro'),
    path('recuperar-password/', forgot_password_screen, name='recuperar_password'),
    path('reset-password/<str:token>/', reset_password_screen, name='reset_password'),
    path('recuperar-pendiente/', pending_reset_screen, name='pendiente_reset'),
    path('main/', main, name='main'),
    path('estadisticas/', statistics, name='estadisticas'),
    path('prediccion/', predict, name='prediccion'),
]
