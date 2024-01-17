from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login ,logout,authenticate
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect ,render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


from django.contrib.auth import login

class RegisterView(FormView):
    template_name = 'account/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        email_subject = "Create Your Account Successfully"
        email_body = render_to_string('account/confirm_email.html', {'user': user})
        email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
        messages.success(self.request, 'Register Successfully!')
        login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Register'
        return context
    




    


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            userpass = form.cleaned_data['password']
            
            user = authenticate(username=name, password=userpass)
            if user is not None:
                login(request, user)
                messages.success(request,'Login Successfully !')
                return redirect('home')  # profile page e redirect korbe
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

        
        




def logout_view(request):
    logout(request)
    messages.success(request,'Logout Successfully !')
    return redirect('login')
