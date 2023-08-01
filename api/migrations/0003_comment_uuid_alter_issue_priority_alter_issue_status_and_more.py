# Generated by Django 4.2.2 on 2023-06-30 04:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_alter_project_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name="issue",
            name="priority",
            field=models.CharField(
                choices=[("low", "LOW"), ("medium", "MEDIUM"), ("high", "HIGH")],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="issue",
            name="status",
            field=models.CharField(
                choices=[
                    ("to_do", "To Do"),
                    ("in_progress", "In Progress"),
                    ("done", "Done"),
                ],
                default="To Do",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="issue",
            name="tag",
            field=models.CharField(
                choices=[("bug", "BUG"), ("feature", "FEATURE"), ("task", "TASK")],
                max_length=20,
            ),
        ),
    ]