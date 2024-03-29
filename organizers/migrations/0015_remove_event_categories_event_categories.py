# Generated by Django 5.0 on 2024-01-17 05:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0014_remove_event_categories_event_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='categories',
        ),
        migrations.AddField(
            model_name='event',
            name='categories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='organizers.category'),
        ),
    ]
