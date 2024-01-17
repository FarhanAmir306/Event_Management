# Generated by Django 5.0 on 2024-01-16 12:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0007_event_attendent'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpcomingEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upcoming_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizers.event')),
            ],
        ),
    ]
