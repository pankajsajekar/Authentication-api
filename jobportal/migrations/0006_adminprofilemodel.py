# Generated by Django 4.1.3 on 2022-11-16 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0005_alter_user_mobile'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminProfileModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=75)),
                ('last_name', models.CharField(max_length=75)),
                ('date_of_birth', models.DateField(blank=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=75)),
                ('state', models.CharField(blank=True, max_length=75)),
                ('country', models.CharField(blank=True, max_length=75)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin_profiles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Admin Profile',
                'verbose_name_plural': 'Admin Profiles',
            },
        ),
    ]
