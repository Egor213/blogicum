# Generated by Django 3.2.16 on 2025-02-13 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_alter_comment_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="comment_count",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
