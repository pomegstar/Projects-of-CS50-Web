from django.urls import path
from . import views

app_name = "appointments"
urlpatterns = [
    path('', views.book, name='book'),
    path('appointment/<int:id>', views.appoint, name='appointment'),
    path('del_ap/<int:id>', views.del_ap, name='del_ap'),
    path('patients', views.patients, name='patients'),
    path('my_all_appointments', views.allap, name='allap'),
    path('pending_appointments', views.pndap, name='pndap'),
    path('my_all_patinets', views.allpat, name='allpat'),

]
