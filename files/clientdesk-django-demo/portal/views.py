from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect, get_object_or_404

from .models import Client, Project


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        auth_login(request, form.get_user())
        return redirect("dashboard")
    return render(request, "portal/login.html", {"form": form})


class PortalLogoutView(LogoutView):
    next_page = "login"


@login_required
def dashboard(request):
    client = get_object_or_404(Client, user=request.user)
    projects = client.projects.all().order_by("-updated_at")
    return render(request, "portal/dashboard.html", {"client": client, "projects": projects})


@login_required
def project_detail(request, pk):
    client = get_object_or_404(Client, user=request.user)
    project = get_object_or_404(Project, pk=pk, client=client)
    return render(request, "portal/project_detail.html", {"project": project})
