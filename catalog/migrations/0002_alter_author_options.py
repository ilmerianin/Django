# Generated by Django 4.1 on 2022-12-31 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="author",
            options={"ordering": ["last_name"]},
        ),
    ]
