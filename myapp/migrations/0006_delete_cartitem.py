# Generated by Django 5.1.3 on 2024-12-11 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_cartitem_options_alter_cartitem_book_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
