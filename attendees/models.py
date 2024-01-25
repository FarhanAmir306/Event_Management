from django.db import models
from django.contrib.auth.models import User
from organizers.models import Event
# Create your models here.

class Attendent(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='attendent')

    def __str__(self):
        return f"Attendent: {self.user.username}"



class Event_Accept(models.Model):
    name=models.ForeignKey(Attendent,on_delete=models.CASCADE)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)

    def __str__(self):
        return f"Attendent: {self.name.user.username}, Event: {self.event.event_name}"




class Profile(models.Model):
    user = models.OneToOneField(Attendent, on_delete=models.CASCADE)
    event = models.ManyToManyField(Event)
