from django.db import models

# Create your models here.

class Project(models.Model):
    name=models.CharField(max_length=50)
    owner=models.ForeignKey(ProductOwner,on_delete=models.CASCADE)
    pb=models.ForeignKey(ProductBacklog, on_delete=models.CASCADE)
    create_time=models.DateField(auto_now=False, auto_now_add=True)


class ProductOwner(models.Model):
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=30)

class  Teammember(models.Model): 
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=30)
    project=models.ForeignKey(Project, on_delete=models.CASCADE)

class ProductBacklog(models.Model):
    pass

class PBI(models.Model):
    card=models.TextField()
    conversation=models.CharField(max_length=100)
    storypoints=models.IntegerField()
    sprintNo=models.IntegerField()
    #define the choices
    inprogress='INP'
    completed='CP'
    notstart='NO'
    stat=[(inprogress,'in progress'),(completed,'compeleted'),(notstart,'not start')]
    status=models.CharField(choices=stat, max_length=20,default=notstart)

class Confirmation(models.Model):
    content=models.CharField(max_length=100)
    done=models.BooleanField()
    pbi=models.ForeignKey(PBI, on_delete=models.CASCADE)


