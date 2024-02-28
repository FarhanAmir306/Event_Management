from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name=models.CharField(max_length=20)
    slug=models.SlugField(max_length=100,null=True)
    
    def __str__(self):
        return self.name

    
class Event(models.Model):
    # user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    event_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=255)
    description = models.TextField()
    categories = models.ForeignKey(Category,on_delete=models.CASCADE, blank=True,null=True,related_name='events')
    tags = models.CharField(max_length=255, blank=True)
    image=models.ImageField(upload_to='organizers/media/',null=True,blank=True)
    attendent=models.IntegerField(default=0)
    is_public = models.BooleanField(default=True) 

    def __str__(self):
        return self.event_name
    




class UpcomingEvent(models.Model):
    event_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=255)
    description = models.TextField()
    categories = models.ManyToManyField(Category, max_length=255, blank=True)
    image=models.ImageField(upload_to='organizers/media/',null=True,blank=True)

    def __str__(self):
        return f"Upcoming: {self.event_name}"


class Comment_Post(models.Model):
    post = models.ForeignKey(Event, on_delete=models.CASCADE,related_name='comments',null=True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comments by {self.name}"