# Generated by Django 5.1.6 on 2025-03-04 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_groupchatmodel_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmodel',
            name='typed',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
