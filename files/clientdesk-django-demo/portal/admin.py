from django.contrib import admin
from .models import Client, Project, ProjectUpdate, Document


class ProjectUpdateInline(admin.TabularInline):
    model = ProjectUpdate
    extra = 1


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("company_name", "user", "phone")
    search_fields = ("company_name", "user__username")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "status", "progress_percent", "updated_at")
    list_filter = ("status",)
    search_fields = ("title", "client__company_name")
    inlines = [ProjectUpdateInline, DocumentInline]


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = ("project", "created_at")


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("label", "project", "uploaded_at")
