from django.contrib import admin

from .models import *

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