# Generated by Django 3.1.4 on 2021-01-16 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='usernumber',
            field=models.CharField(max_length=4),
        ),
    ]
