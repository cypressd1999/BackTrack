# Generated by Django 2.2.1 on 2019-11-22 06:46

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
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
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
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
                ('pbi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backtrack.PBI')),
                ('sprint_backlog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backtrack.SprintBacklog')),
            ],
        ),
        migrations.CreateModel(
            name='ScrumMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backtrack.Project')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
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
        migrations.AddField(
            model_name='developer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
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
