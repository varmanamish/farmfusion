# Generated by Django 5.1.6 on 2025-02-21 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("businessmodel", "0003_alter_investmentmodel_profit_generated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="investmentmodel",
            name="estimated_time",
            field=models.CharField(),
        ),
    ]
