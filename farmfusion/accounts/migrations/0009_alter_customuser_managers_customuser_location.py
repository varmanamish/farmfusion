# Generated by Django 5.1.6 on 2025-02-21 10:13

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_wallet_wallet_pin'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
