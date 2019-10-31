from django.db import models

# Create your models here.

class ProductOwner(models.Model):
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=30)

class ProductBacklog(models.Model):
    pass

class Project(models.Model):
    name=models.CharField(max_length=50)
    owner=models.ForeignKey(ProductOwner,on_delete=models.CASCADE)
    pb=models.ForeignKey(ProductBacklog, on_delete=models.CASCADE)
    create_time=models.DateField(auto_now=False, auto_now_add=True)

class  TeamMember(models.Model): 
    name=models.CharField(max_length=20)
    email=models.EmailField()

class PBI(models.Model):
    title=models.CharField(max_length=20, null=True)
    card=models.TextField(blank=True, null=True)
    conversation=models.CharField(max_length=100, \
        blank=True, null=True)
    storypoints=models.IntegerField(blank=True, null=True)
    """
    sprintNo=models.IntegerField()
    #define the choices
    inprogress='INP'
    completed='CP'
    notstart='NO'
    stat=[(inprogress,'in progress'),(completed,'compeleted'),(notstart,'not start')]
    status=models.CharField(choices=stat, max_length=20,default=notstart)
    """

class Confirmation(models.Model):
    content=models.CharField(max_length=100)
    done=models.BooleanField()
    pbi=models.ForeignKey(PBI, on_delete=models.CASCADE)


