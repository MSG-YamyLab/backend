# Generated by Django 5.1.6 on 2025-03-07 12:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_usermodel_contacts_alter_usermodel_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaDataModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_style', models.JSONField()),
            ],
            options={
                'db_table': 'meta_data',
            },
        ),
        migrations.AddField(
            model_name='usermodel',
            name='block_users',
            field=models.ManyToManyField(blank=True, null=True, related_name='block_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='contacts',
            field=models.ManyToManyField(blank=True, null=True, related_name='contact_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='meta_data',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.metadatamodel'),
        ),
    ]
