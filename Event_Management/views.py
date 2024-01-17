from django.views.generic import TemplateView
from organizers.models import Event,Category,UpcomingEvent
from django.views.generic import ListView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
class HomeView(TemplateView):
    template_name = "index.html"

# class EventList(ListView):
#     model = Event
#     template_name='index.html'
#     context_object_name = 'events'



# def category_view(request):
#     categories = Category.objects.all()
#     events = Event.objects.all()
#     context = {'categories': categories, 'events': events}
#     return render(request, 'index.html', context)






def category_view(request, category_slug=None):
    categories = Category.objects.all()
    events = Event.objects.all()
    upcoming = Event.objects.filter()
    print(category_slug)
    if category_slug is not None:
        category = Category.objects.filter(slug=category_slug).first()
        events = Event.objects.filter(categories=category)

    return render(request, 'index.html', {'categories': categories, 'events': events, 'upcomings': upcoming})
