# Generated by Django 3.1.1 on 2020-10-20 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='read',
            field=models.IntegerField(default=0),
        ),
    ]
