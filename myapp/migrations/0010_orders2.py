# Generated by Django 5.1.3 on 2024-12-13 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_cartitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders2',
            fields=[
                ('order_id', models.IntegerField(db_column='Order_id', primary_key=True, serialize=False)),
                ('order_date', models.DateField(blank=True, db_column='Order_date', null=True)),
                ('shipped_date', models.DateField(blank=True, db_column='Shipped_Date', null=True)),
                ('status', models.CharField(blank=True, db_column='Status', max_length=20, null=True)),
                ('from_employee', models.IntegerField(blank=True, db_column='From_employee', null=True)),
            ],
            options={
                'db_table': 'orders2',
                'managed': False,
            },
        ),
    ]
