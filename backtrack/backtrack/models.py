from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save

class User(AbstractUser):
    PRODUCTOWNER = 'PO'
    DEVELOPER = 'DEV'
    SCRUMMASTER = 'SM'
    ADMIN = 'ADMIN'
    ROLE_CHOICES = [
        (PRODUCTOWNER, 'product owner'),
        (DEVELOPER, 'developer'),
        (SCRUMMASTER, 'scrum master'),
        (ADMIN, 'administrator')
    ]
    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=20,
        default=ADMIN
    )

class ProductOwner(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, models.CASCADE)

    def __str__(self):
        return self.user.username

class Project(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    start_time = models.DateTimeField(auto_now_add=True)
    product_owner = models.ForeignKey(
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

    def __str__(self):
        return self.user.username

class ScrumMaster(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, models.CASCADE)
    project = models.ForeignKey(
        Project,
        models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username

class ProductBacklog(models.Model):
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
        return self.title

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
    pbi = models.ManyToManyField(PBI)
    is_current_sprint = models.BooleanField(default=False)
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

    def get_absolute_url(self):
        return reverse('backtrack:view sb',
            kwargs={
            'project_name': \
                self.pbi.all()[0].product_backlog.project.name
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

def user_post_save_receiver(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.DEVELOPER:
            Developer.objects.create(user=instance)
        elif instance.role == User.PRODUCTOWNER:
            ProductOwner.objects.create(user=instance)
        elif instance.role == User.SCRUMMASTER:
            ScrumMaster.objects.create(user=instance)

post_save.connect(user_post_save_receiver,
    sender=settings.AUTH_USER_MODEL)