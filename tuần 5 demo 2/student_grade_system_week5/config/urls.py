from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from core_views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", dashboard, name="dashboard"),
    path("students/", include("students.urls")),
    path("academics/", include("academics.urls")),
    path("enrollments/", include("enrollments.urls")),
    path("grading/", include("grading.urls")),
]
