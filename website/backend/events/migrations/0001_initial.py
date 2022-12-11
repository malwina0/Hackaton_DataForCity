# Generated by Django 4.1.3 on 2022-11-18 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.JSONField(blank=True, null=True)),
                ('url', models.TextField(blank=True, max_length=500, null=True)),
                ('map', models.JSONField(blank=True, null=True)),
                ('category', models.JSONField(blank=True, null=True)),
                ('occurrence', models.JSONField(blank=True, null=True)),
                ('lead', models.TextField(blank=True, max_length=500, null=True)),
                ('title', models.TextField(blank=True, max_length=500, null=True)),
                ('address', models.JSONField(blank=True, null=True)),
                ('language', models.TextField(blank=True, max_length=200, null=True)),
                ('text', models.TextField(blank=True, max_length=500, null=True)),
                ('availableLanguages', models.JSONField(blank=True, null=True)),
                ('localization', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]
