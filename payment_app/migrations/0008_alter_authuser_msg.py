# Generated by Django 4.1.3 on 2023-05-14 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment_app", "0007_alter_authuser_group_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="authuser",
            name="msg",
            field=models.TextField(blank=True, default="", null=True),
        ),
    ]