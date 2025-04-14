from django.contrib import admin
from . models import Attendee , Ticket , Event

# Register your models here.



admin.site.register(Attendee)
admin.site.register(Ticket)
admin.site.register(Event)