from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *

class ProductOwnerInline(admin.StackedInline):
    model = ProductOwner
    verbose_name_plural = "product owner"

class DeveloperInline(admin.StackedInline):
    model = Developer
    verbose_name_plural = "developer"

class ScrumMasterInline(admin.StackedInline):
    model = ScrumMaster
    verbose_name_plural = "scrum master"

class UserAdmin(BaseUserAdmin):
    inlines = (ProductOwnerInline, DeveloperInline, ScrumMasterInline)

admin.site.register(User, UserAdmin)

class ProjectAdmin(admin.ModelAdmin):
    admin.site.register(Project)
    list_display = ('name', 'start_time', 'product_owner')

class ProductBacklogAdmin(admin.ModelAdmin):
    admin.site.register(ProductBacklog)
    list_display = (
        'total_story_points',
        'remaining_story_points',
        'total_number_of_pbi',
        'project'
    )

class PBIAdmin(admin.ModelAdmin):
    admin.site.register(PBI)
    list_display = (
        'title',
        'card',
        'conversation',
        'storypoints',
        'priority',
        'status',
        'product_backlog'
    )

class SBAdmin(admin.ModelAdmin):
    admin.site.register(SprintBacklog)

class TaskAdmin(admin.ModelAdmin):
    admin.site.register(Task)

class ConfirmationAdmin(admin.ModelAdmin):
    admin.site.register(Confirmation)