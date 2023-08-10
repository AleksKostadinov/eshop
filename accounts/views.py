from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from accounts.forms import RegisterForm
from accounts.models import Account, UserProfile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from orders.models import Order


# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = auth.authenticate(username=username, password=password)
#         if user:
#             auth.login(request, user)
#             messages.success(request, 'You have successfully logged in!')
#             return redirect('shop_app:home')

#         else:
#             messages.error(request, 'Invalid credentials')
#     return render(request, 'accounts/login.html')



class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(LogoutView):
    template_name = "accounts/logout.html"

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
        messages.success(self.request, 'Registration successful.')

        return super().form_valid(form)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user=self.request.user

        orders = Order.objects.order_by('-created_at').filter(user=user, is_ordered=True)
        orders_count = orders.count()
        userprofile = UserProfile.objects.get(user=user)
        context['orders'] = orders
        context['orders_count'] = orders_count
        context['userprofile'] = userprofile

        return context

