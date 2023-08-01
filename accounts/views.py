from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import login, authenticate


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


class CustomRegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')  # Replace 'home' with the URL name of your home page

    def form_valid(self, form):
        # Save the new user object
        form.save()
        # Log the user in after registration
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)
