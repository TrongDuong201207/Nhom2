from django.urls import path
from . import views
app_name = 'academics'
urlpatterns = [
    path('courses/', views.course_list, name='courses'),
    path('courses/add/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_update, name='course_update'),
    path('sections/', views.section_list, name='sections'),
    path('sections/add/', views.section_create, name='section_create'),
    path('sections/<int:pk>/edit/', views.section_update, name='section_update'),
    path('sections/<int:pk>/close/', views.section_close, name='section_close'),
]
