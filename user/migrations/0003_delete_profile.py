# Generated by Django 5.1.3 on 2024-11-30 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_profile_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
