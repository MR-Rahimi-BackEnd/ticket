# Generated by Django 5.1.7 on 2025-03-16 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_event_attendee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attendee',
            field=models.ManyToManyField(blank=True, to='ticket.attendee'),
        ),
    ]
