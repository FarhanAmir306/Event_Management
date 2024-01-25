from typing import Any
from django.shortcuts import render,redirect
from .import forms
from .import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView,UpdateView,DetailView,ListView,DeleteView
from django.urls import reverse_lazy
from attendees.models import Event_Accept ,Attendent,Profile
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



# class AddCreateView(CreateView):
#     model=models.Event
#     form_class=forms.EventForm
#     template_name = 'organizers/event_add.html'
#     success_url=reverse_lazy('home')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         messages.success(self.request, "The Event was created successfully.")
#         return super().form_valid(form)




class EventList(LoginRequiredMixin,ListView):
    model = models.Event
    context_object_name = 'events'


@login_required
def profile(request,category_slug=None):
    attendent_instance, created = Attendent.objects.get_or_create(user=request.user)
    # user_profile, created = Profile.objects.get_or_create(user=attendent_instance)
    # events = user_profile.event.all()
    categories = models.Category.objects.all()
    
    profile_events=Event_Accept.objects.filter(name=attendent_instance)
   
    if category_slug is not None:
        category = models.Category.objects.filter(slug=category_slug).first()
        events=models.Event.objects.filter(categories=category)
        profile_events=[]
        for event in events:
            accept_event=Event_Accept.objects.filter(event=event).first()
            print(accept_event)
            if accept_event is not None:
                profile_events.append(accept_event)
        
    
    return render(request, 'organizers/profile.html', { 'profile_events': profile_events,'categories':categories})






class ProfileUpdate(LoginRequiredMixin,UpdateView):
    model = User
    form_class=forms.UserChange
    # fields = ['username','first_name','last_name']
    template_name='organizers/edit_profile.html'
    success_url = reverse_lazy('home')
    
    def get_object(self,queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your Profile updated successfully.")
        return super(ProfileUpdate,self).form_valid(form)


    


@login_required
def password_reset_by_user(request):
    form = PasswordChangeForm(user=request.user ,data=request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Password Change successfully !.")
        update_session_auth_hash(request, form.user)
        return redirect('/')
    return render(request, 'organizers/password_change.html', {'form': form})

@login_required
def attendent_event(request, id):
    event = get_object_or_404(models.Event, id=id)
    my_events=Event_Accept.objects.filter(event=event)
    if not my_events:
        attendent_instance, created = Attendent.objects.get_or_create(user=request.user)
        event_accept, created = Event_Accept.objects.get_or_create(event=event, name=attendent_instance)
        if not created:
            messages.error(request, "Sorry event not created !")

        event_accept.save()
        event.attendent += 1


    #ekhane profile e event save korar jonno lekha hoyeche 
    # user_profile, created = Profile.objects.get_or_create(user=attendent_instance)
    # # print(user_profile.event)
    # user_profile.event.add(event)
    # print(user_profile.event.all())
        event.save()
    else:
        messages.success(request,"Sorry Event Already accepted !")
    return redirect('home')


@login_required
def attendent_decline(request, id):
    event = get_object_or_404(models.Event, id=id)
    messages.success(request, "Cencel Event Successfully !.")
    return redirect('home')




class EventDetailsView(LoginRequiredMixin,DetailView):
    model = models.Event
    template_name='organizers/event_details.html'
    pk_url_kwarg='id'



from django.shortcuts import get_object_or_404

def TaskDelete(request, id):
    event_accept=Event_Accept.objects.filter(id=id)
    event_accept.delete()
    return redirect('profile')
    
    