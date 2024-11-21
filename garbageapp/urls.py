from django.urls import path
from . import views
 
app_name = 'garbageapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('types/', views.types, name='types'),
    path('booking/', views.booking, name='booking'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('map/', views.map, name='map'),
    # path('')
    path('plant/<int:plant_id>/', views.plant, name='plant'), 
    path('payment/',views.payment,name='payment'),
    path('success/',views.success,name='success'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<uuid:token>/', views.reset_password, name='reset_password'),
    
]