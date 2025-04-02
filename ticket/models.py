from django.db import models


class Attendee(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254 , unique=True)
    
    def __str__(self):
        return f'{self.name}' 

class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now=False, auto_now_add=False)
    location = models.TextField()
    participants = models.IntegerField(default=0)
    max_participants = models.IntegerField()
    attendee = models.ManyToManyField(Attendee , blank=True)
    def __str__(self):
        return f'{self.title} -- {self.id}'
    



    
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f'{self.id}'
    