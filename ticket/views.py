from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from django.core.cache import cache
from ticket.permissions import IsSuperUser
from . models import Ticket, Event , Attendee
from . serializers import TicketSerizlizer , EventSerizlizer , AttendeeSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import permissions
# Create your views here.


class CacheTestViewSet(viewsets.ViewSet):

    def list (self, request):
        n = int(request.query_params.get('n', 0))
        result = self.fibonacci(n)
        return Response({'n': n, 'fibonacci': result})

    def fibonacci(self, n):
        if n <= 1:
            return n

        cached_value = cache.get(f'fib_{n}')
        if cached_value is not None:
            return cached_value

        value = self.fibonacci(n - 1) + self.fibonacci(n - 2)
        
        cache.set(f'fib_{n}', value, timeout=None)

        return value


class EventViewSet(viewsets.ViewSet):
    querset = Event.objects.all()
    
    # def list(self , request):
    #     queryset = Event.objects.prefetch_related('attendee')
    #     # queryset = Event.objects.all()
        
    #     serializer = EventSerizlizer(queryset ,  many = True)
        
    #     return Response (serializer.data)
    
    
    def list(self, request):
        queryset = Event.objects.all()
        events_with_views = []

        for event in queryset:
            key = f'event_{event.id}_views'

            # اگر کلید هنوز وجود نداره، مقدار اولیه بذار
            if not cache.get(key):
                cache.set(key, 0)

            # افزایش تعداد بازدید
            new_views = cache.incr(key)

            # سریالایز و اضافه کردن مقدار جدید بازدید
            event_data = EventSerizlizer(event).data
            event_data['views'] = new_views

            events_with_views.append(event_data)

        return Response(events_with_views)



    
    
    @action(detail=False , methods = ['POST'])
    def post_event(self , request):
        serializer = EventSerizlizer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def retrieve(self,request , pk=None):
        queryset = Event.objects.filter(pk=pk)
        serializer = EventSerizlizer(queryset)
        
        return Response(serializer.data)
    
    def destroy(self , requset , pk=None):
        event = Event.objects.filter(pk=pk)
        event.delete()
        return Response('event is delete')
    
    
class AttendeeViewSet(viewsets.ViewSet):
    queryset = Attendee.objects.all()
    permission_classes = [IsSuperUser]
    
    
    def post(self,request):
        name = request.data.get('name')
        email = request.data.get('email')
        
        
        if Attendee.objects.filter(email = email).exists():
            return Response({'error': 'This email is already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        
        serializer = AttendeeSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
      
    def list(self , request):
        queryset = Attendee.objects.all()
        serializer = AttendeeSerializer(queryset ,  many = True)
        
        return Response (serializer.data)
                   
        
    def retrieve(self,request , pk=None):
        queryset = Attendee.objects.filter(pk=pk)
        serializer = AttendeeSerializer(queryset)
        
        return Response(serializer.data)
    
    def destroy(self , requset , pk=None):
        event = Attendee.objects.filter(pk=pk)
        event.delete()
        return Response('event is delete')
        
        
        
class TicketViewSet(viewsets.ViewSet):
    
    def list(self,request):
        queryset = Ticket.objects.select_related('event' , 'attendee')
        serializer = TicketSerizlizer(queryset,many=True)
        return Response (serializer.data)
    
    def post(self, request, *args, **kwargs):
        event_id = request.data.get('event_id')
        attendee_id = request.data.get('attendee_id')

        # print(f'event_id: {event_id}, attendee_id: {attendee_id}') 

        if not event_id or not attendee_id:
            return Response({'error': 'Event ID and Attendee ID are required'}, status=status.HTTP_400_BAD_REQUEST)

        event_id = int(event_id)
        attendee_id = int(attendee_id)

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            attendee = Attendee.objects.get(id=attendee_id)
        except Attendee.DoesNotExist:
            return Response({'error': 'Attendee not found'}, status=status.HTTP_404_NOT_FOUND)

        if event.participants >= event.max_participants:
            return Response({'error': 'Event is full'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        event.participants +=1
        event.save()
        event.attendee.add(attendee)
        event.save()

        ticket = Ticket.objects.create(event=event, attendee=attendee)

        return Response({'message': 'Ticket created successfully'}, status=status.HTTP_201_CREATED)
