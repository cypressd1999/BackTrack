# Generated by Django 2.2.1 on 2019-11-08 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PBI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('card', models.TextField(blank=True, null=True)),
                ('conversation', models.TextField(blank=True, null=True)),
                ('storypoints', models.IntegerField(blank=True, null=True)),
                ('priority', models.IntegerField(default=1)),
                ('status', models.CharField(choices=[('INP', 'in progress'), ('FN', 'finished'), ('NO', 'not started')], default='NO', max_length=20)),
            ],
            options={
                'ordering': ('priority',),
            },
        ),
        migrations.CreateModel(
            name='ProductOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('prodcut_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backtrack.ProductOwner')),
            ],
        ),
        migrations.CreateModel(
            name='SprintBacklog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sprint_number', models.IntegerField()),
                ('hours_available', models.IntegerField(default=0)),
                ('remaining_hours', models.FloatField(default=0)),
                ('is_current_sprint', models.BooleanField(default=False)),
                ('pbi', models.ManyToManyField(to='backtrack.PBI')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('total_hours', models.FloatField(default=0)),
                ('finished_hours', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('INP', 'in progress'), ('FN', 'finished'), ('NO', 'not started')], default='NO', max_length=20)),
                ('developer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backtrack.Developer')),
                ('sprint_backlog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backtrack.SprintBacklog')),
            ],
        ),
        migrations.CreateModel(
            name='ScrumMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backtrack.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductBacklog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_story_points', models.IntegerField(default=0)),
                ('remaining_story_points', models.IntegerField(default=0)),
                ('total_number_of_pbi', models.IntegerField(default=0)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backtrack.Project')),
            ],
        ),
        migrations.AddField(
            model_name='pbi',
            name='product_backlog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backtrack.ProductBacklog'),
        ),
        migrations.AddField(
            model_name='developer',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backtrack.Project'),
        ),
        migrations.CreateModel(
            name='Confirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('done', models.BooleanField()),
                ('pbi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backtrack.PBI')),
            ],
        ),
    ]
