# Generated by Django 3.2.7 on 2021-09-23 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('manaba_id', models.CharField(blank=True, max_length=30, null=True)),
                ('manaba_password', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
    ]
