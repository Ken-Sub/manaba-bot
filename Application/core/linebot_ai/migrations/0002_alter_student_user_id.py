# Generated by Django 3.2.7 on 2021-09-23 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linebot_ai', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user_id',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
