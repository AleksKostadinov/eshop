from django import forms
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView
from accounts.forms import AccountForm, ChangePasswordForm, RegisterForm, UserProfileForm
from accounts.models import Account, SubscribedUsers, UserProfile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.validations import clean_first_name, clean_last_name, clean_password, clean_phone_number
from orders.models import Order, OrderProduct
from django.contrib.auth import login
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['user_logged_in'] = request.user.is_authenticated
        return self.render_to_response(context)

    def form_invalid(self, form):
        if 'email' in form.errors and 'already in use' in form.errors['email'][0].lower():
            messages.error(self.request, 'This email is already associated with another account.')
        else:
            messages.error(self.request, 'Invalid username or password')

        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(LogoutView):
    template_name = "accounts/logout.html"


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

        # Check if a user with the provided email already exists
        if Account.objects.filter(email=email).exists():
            # User with this email already exists, set an error message
            messages.error(self.request, 'This email is already in use.')
            return render(self.request, self.template_name, {'form': form})

        # Create the new user
        user = Account.objects.create_user(
            first_name=first_name, last_name=last_name,
            email=email, phone_number=phone_number,
            username=username, password=password
        )

        backend = settings.CUSTOM_AUTHENTICATION_BACKEND
        login(self.request, user, backend=backend)
        messages.success(self.request, 'Registration successful.')

        return super().form_valid(form)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user=self.request.user
        user_email = user.email
        is_subscribed = SubscribedUsers.objects.filter(email=user_email).exists()


        orders = Order.objects.order_by('-created_at').filter(user=user, is_ordered=True)
        orders_count = orders.count()
        userprofile = UserProfile.objects.get(user=user)
        context['orders'] = orders
        context['orders_count'] = orders_count
        context['userprofile'] = userprofile
        context['is_subscribed'] = is_subscribed

        return context

class MyOrdersView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/my_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(user=self.request.user, is_ordered=True).order_by('-created_at')
        context['orders'] = orders
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/edit_profile.html'
    form_class = AccountForm
    profile_form_class = UserProfileForm
    model = UserProfile
    success_url = reverse_lazy('accounts:edit_profile')

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_form'] = self.form_class(instance=self.request.user)
        context['profile_form'] = self.profile_form_class(instance=self.request.user.userprofile)
        return context

    def form_valid(self, form):
        account_form = self.form_class(self.request.POST, instance=self.request.user)
        profile_form = self.profile_form_class(self.request.POST, self.request.FILES, instance=self.request.user.userprofile)

        if account_form.is_valid() and profile_form.is_valid():
            try:
                account_form.cleaned_data['phone_number'] = clean_phone_number(account_form.cleaned_data['phone_number'])
                account_form.cleaned_data['first_name'] = clean_first_name(account_form.cleaned_data['first_name'])
                account_form.cleaned_data['last_name'] = clean_last_name(account_form.cleaned_data['last_name'])

                account_form.save()
                profile_form.save()
                messages.success(self.request, 'Your profile has been updated.')
            except forms.ValidationError as e:
                for error_msg in e.error_list:
                    for msg in error_msg.messages:
                        messages.error(self.request, msg)

        return super().form_valid(form)


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'accounts/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('accounts:change_password')

    def form_valid(self, form):
        current_password = form.cleaned_data['current_password']
        new_password = form.cleaned_data['new_password']
        confirm_password = form.cleaned_data['confirm_password']

        user = self.request.user
        success = user.check_password(current_password)

        if success:
            if current_password == new_password:
                messages.error(self.request, 'New password cannot be same as current password.')
                return self.form_invalid(form)
            elif new_password == confirm_password:
                try:
                    clean_password(new_password)
                    user.set_password(new_password)
                    user.save()
                    messages.success(self.request, 'Password updated successfully.')
                except forms.ValidationError as e:
                    for error_msg in e.error_list:
                        for msg in error_msg.messages:
                            messages.error(self.request, msg)
            else:
                messages.error(self.request, 'Password does not match!')
        else:
            messages.error(self.request, 'Please enter a valid current password.')

        return super().form_valid(form)


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/order_detail.html'
    model = Order

    def get_object(self, queryset=None):
        order_number = self.kwargs.get('order_number')
        return Order.objects.get(order_number=order_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order_detail = OrderProduct.objects.filter(order__order_number=self.object.order_number)
        sub_total = sum(item.product_price * item.quantity for item in order_detail)

        context["order_detail"] = order_detail
        context["sub_total"] = sub_total
        return context


class SubscribeView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', None)

        if not email:
            messages.error(request, "You must type a valid name and email to subscribe to the Newsletter")
            return redirect("/")

        # if get_user_model().objects.filter(email=email).first():
        #     messages.error(request, f"A registered user with the email {email} already exists.")
        #     return redirect(request.META.get("HTTP_REFERER", "/"))

        subscribe_user = SubscribedUsers.objects.filter(email=email).first()

        if subscribe_user:
            messages.error(request, f"The email address {email} is already subscribed.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect("/")

        subscribe_model_instance = SubscribedUsers()
        subscribe_model_instance.email = email
        subscribe_model_instance.save()
        messages.success(request, f'The email {email} was successfully subscribed to our newsletter!')
        return redirect(request.META.get("HTTP_REFERER", "/"))


class UnsubscribeView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', None)

        if not email:
            messages.error(request, "You must provide a valid email to unsubscribe from the Newsletter")
            return redirect("/")

        subscribe_user = SubscribedUsers.objects.filter(email=email).first()
        if not subscribe_user:
            messages.error(request, f"The email address {email} is not subscribed.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        subscribe_user.delete()
        messages.success(request, f'The email {email} was successfully unsubscribed from our newsletter.')
        return redirect(request.META.get("HTTP_REFERER", "/"))

