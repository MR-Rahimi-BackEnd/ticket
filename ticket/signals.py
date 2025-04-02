from django.dispatch import Signal, receiver
from django.db.models.signals import post_save

from ticket.models import Ticket



@receiver(post_save, sender=Ticket)
def update_event_participants(sender, instance, created, **kwargs):
    if created:
        event = instance.event
        event.participants += 1
       
        event.save()
        