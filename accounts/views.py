from django import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from accounts.forms import AccountForm, ChangePasswordForm, RegisterForm, UserProfileForm
from accounts.models import Account, UserProfile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.validations import clean_password
from orders.models import Order
from django.contrib.auth import login
from django.views.generic.edit import UpdateView


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
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

        user = Account.objects.create_user(
            first_name=first_name, last_name=last_name,
            email=email, phone_number=phone_number,
            username=username, password=password
            )
        user.save()

        login(self.request, user)
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

class MyOrdersView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/my_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(user=self.request.user, is_ordered=True).order_by('-created_at')
        context['orders'] = orders
        return context

# class EditProfileView(LoginRequiredMixin, TemplateView):
#     template_name = 'accounts/edit_profile.html'

#     def post(self, request, *args, **kwargs):
#         userprofile = get_object_or_404(UserProfile, user=request.user)
#         account_form = AccountForm(request.POST, instance=request.user)
#         profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

#         if account_form.is_valid() and profile_form.is_valid():
#             account_form.save()
#             profile_form.save()
#             messages.success(request, 'Your profile has been updated.')
#             return redirect('accounts:edit_profile')

#         context = {
#             'account_form': account_form,
#             'profile_form': profile_form,
#             'userprofile': userprofile,
#         }
#         return render(request, self.template_name, context)

#     def get(self, request, *args, **kwargs):
#         userprofile = get_object_or_404(UserProfile, user=request.user)
#         account_form = AccountForm(instance=request.user)
#         profile_form = UserProfileForm(instance=userprofile)
#         context = {
#             'account_form': account_form,
#             'profile_form': profile_form,
#             'userprofile': userprofile,
#         }
#         return render(request, self.template_name, context)

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
            account_form.save()
            profile_form.save()
            messages.success(self.request, 'Your profile has been updated.')

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
                    messages.error(self.request, e)
                    return self.form_invalid(form)
            else:
                messages.error(self.request, 'Password does not match!')
        else:
            messages.error(self.request, 'Please enter a valid current password.')

        return super().form_valid(form)
