from rest_framework import serializers
from .models import Attendee , Event , Ticket





class EventSerizlizer(serializers.ModelSerializer):
    # ateendee = serializers.
    class Meta:
        model = Event
        fields = ['id' , 'title' , 'location' , 'date' , 'max_participants' , 'attendee']
        
class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = [ 'id', 'name' , 'email' ]
        
class TicketSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id' , 'event' , 'attendee']