from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView
from accounts.forms import RegisterForm
from accounts.models import Account


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('shop_app:home')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        return response

# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             email = form.cleaned_data['email']
#             phone_number = form.cleaned_data['phone_number']
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']

#             user = Account.objects.create_user(first_name=first_name, last_name=last_name,
#                                                email=email, phone_number=phone_number,
#                                                username=username, password=password)
#             user.save()
#     else:
#         form = RegisterForm()

#     return render(request, 'accounts/register.html', {'form': form})

class CustomRegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('shop_app:home')

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = Account.objects.create_user(
            first_name=first_name, last_name=last_name,
            email=email, phone_number=phone_number,
            username=username, password=password
            )
        user.save()

        return super().form_valid(form)
