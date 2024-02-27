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
from django.views import View


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


    

class PostView(View,LoginRequiredMixin):
    template_name = 'organizers/comment.html'
    
   

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(models.Event, pk=kwargs['pk'])
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            comment_form.instance.name = request.user.username
            comment_form.instance.email = request.user.email
            print(new_comment)
            new_comment.save()

        return self.get(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(models.Event, pk=kwargs['pk'])
        comments = post.comments.all()
        print(comments)
        comment_form = forms.CommentForm()
        return render(request, self.template_name, {'comment_form': comments , 'comment_input':comment_form})
    
    
    
    



def edit_comment(request,id,post_id):
    user = request.user
    # print(user.username)
    post_cl = models.Event.objects.get(id=post_id)
    # print(post_cl.caption)
    if models.Comment_Post.objects.filter(id=id,name=user.username,email=user.email).exists():
        comment = models.Comment_Post.objects.get(id=id,name=user.username,email=user.email)
        # print(comment.body)
        # return redirect('homepage')
        # comment = Comment.objects.get(pk=id)
        form = forms.CommentForm(instance=comment)
        # print(post.name)
        if request.method == 'POST':
            form = forms.CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                messages.success(request,'Comment updated successfully')
                return redirect('comment',pk=post_cl.id)
        else:
            form = forms.CommentForm(instance=comment)
        return render(request, 'organizers/edit_comment.html',{'form': form,'text':'Comment Edit'})
    
     
    
    else:
        messages.error(request,'You Can not edit another user comment')
        return redirect('comment',pk=post_cl.id)
    


def delete_comment(request,id,post_id):
    user = request.user
    
    post_cl = models.Event.objects.get(id=post_id)
    
    if models.Comment_Post.objects.filter(id=id,name=user.username,email=user.email).exists():
        comment =models.Comment_Post.objects.get(id=id,name=user.username,email=user.email)
        comment.delete()
        messages.success(request,'Comment Deleted Successfully')
        return redirect('comment',pk=post_cl.id)
    
    
    
    
    else:
        messages.error(request,'You Can not Delete another user comment')
        return redirect('comment',pk=post_cl.id)
    