from django.urls import path
from . import views
app_name = 'enrollments'
urlpatterns = [
    path('', views.enrollment_list, name='list'),
    path('add/', views.enrollment_create, name='create'),
]
