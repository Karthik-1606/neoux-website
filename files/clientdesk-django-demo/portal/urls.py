from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.PortalLogoutView.as_view(), name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),
]
