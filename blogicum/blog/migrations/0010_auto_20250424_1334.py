# Generated by Django 3.2.16 on 2025-04-24 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0009_alter_post_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={
                "ordering": ("created_at",),
                "verbose_name": "комментарий",
                "verbose_name_plural": "Комментарии",
            },
        ),
        migrations.RemoveField(
            model_name="post",
            name="comment_count",
        ),
    ]
