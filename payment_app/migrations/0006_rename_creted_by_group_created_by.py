# Generated by Django 4.1.3 on 2023-05-14 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payment_app", "0005_remove_authuser_group_authuser_group_name_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="group",
            old_name="creted_by",
            new_name="created_by",
        ),
    ]
