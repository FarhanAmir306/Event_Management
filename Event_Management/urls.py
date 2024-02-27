"""
URL configuration for Event_Management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views
admin.site.site_header="Harmony Event Management Admin Panel"
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.HomeView.as_view(),name='home'),
    path('', views.category_view,name='home'),
    path('category/<slug:category_slug>/', views.category_view,name='cat'),
    path('account/',include('account.urls')),
    path('event/',include('organizers.urls')),
    path('about/',TemplateView.as_view(template_name="about.html"),name='about'),
    path('speaker/',TemplateView.as_view(template_name="speaker.html"),name='speek'),
    path('project/',views.MyallEvent,name='project'),
    path('contact/',TemplateView.as_view(template_name="contact.html"),name='contact'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


