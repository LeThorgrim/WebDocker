# Generated by Django 5.1.2 on 2024-10-25 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediafile',
            name='folder',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
