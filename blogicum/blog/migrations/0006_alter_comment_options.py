# Generated by Django 3.2.16 on 2025-02-13 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0005_post_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"ordering": ("created_at",)},
        ),
    ]
