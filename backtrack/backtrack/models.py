from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    pass

class ProductOwner(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, models.CASCADE)

class Project(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    start_time = models.DateTimeField(auto_now_add=True)
    prodcut_owner = models.ForeignKey(
        ProductOwner,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return "Project %s" % self.name

    def get_absolute_url(self):
        return reverse('backtrack:view pb',
            kwargs={'project_name': self.name}
        )

class Developer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, models.CASCADE)
    project = models.ForeignKey(
        Project,
        models.SET_NULL,
        blank=True,
        null=True
    )

class ScrumMaster(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, models.CASCADE)
    project = models.ForeignKey(
        Project,
        models.SET_NULL,
        blank=True,
        null=True
    )

class ProductBacklog(models.Model):
    total_story_points = models.IntegerField(default=0)
    remaining_story_points = models.IntegerField(default=0)
    total_number_of_pbi = models.IntegerField(default=0)
    project = models.OneToOneField(Project, models.CASCADE)

    def __str__(self):
        return "PB belonging to project %s" % self.project.name

class PBI(models.Model):
    title = models.CharField(max_length=20)
    card = models.TextField(blank=True, null=True)
    conversation = models.TextField(blank=True, null=True)
    storypoints = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(default=1)
    #define the choices
    INPROGRESS = 'INP'
    FINISHED = 'FN'
    NOTSTARTED = 'NO'
    STATUS_CHOICES = [
        (INPROGRESS, 'in progress'),
        (FINISHED, 'finished'),
        (NOTSTARTED, 'not started')
    ]
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=20,
        default=NOTSTARTED
    )
    product_backlog = models.ForeignKey(
        ProductBacklog, models.CASCADE
    )

    def __str__(self):
        return "title: %s" % self.title

    def get_absolute_url(self):
        return reverse('backtrack:view pb',
            kwargs={
            'project_name': self.product_backlog.project.name
            }
        )

    class Meta:
        ordering = ('priority',)

class Confirmation(models.Model):
    content = models.CharField(max_length=100)
    done = models.BooleanField()
    pbi = models.ForeignKey(PBI, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('backtrack:view pbi', kwargs={
            'pk': self.pbi.pk
        })

class SprintBacklog(models.Model):
    sprint_number = models.IntegerField()
    hours_available = models.IntegerField(default=0)
    remaining_hours = models.FloatField(default=0)
    pbi = models.ManyToManyField(PBI)
    is_current_sprint = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('backtrack:view sb',
            kwargs={
            'project_name': self.pbi.all()[0].product_backlog.project.name
        }
        )

class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    total_hours = models.FloatField(default=0)
    finished_hours = models.FloatField(default=0)
    INPROGRESS = 'INP'
    FINISHED = 'FN'
    NOTSTARTED = 'NO'
    STATUS_CHOICES = [
        (INPROGRESS, 'in progress'),
        (FINISHED, 'finished'),
        (NOTSTARTED, 'not started')
    ]
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=20,
        default=NOTSTARTED
    )
    sprint_backlog = models.ForeignKey(
        SprintBacklog,
        models.CASCADE
    )
    pbi = models.ForeignKey(PBI, models.CASCADE)
    developer = models.ForeignKey(
        Developer,
        models.SET_NULL,
        blank=True,
        null=True
    )

    def get_absolute_url(self):
        return reverse('backtrack:view task',
            kwargs={'pk': self.sprint_backlog.id}
        )