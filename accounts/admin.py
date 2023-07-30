from django.contrib import admin
from accounts.models import Account, UserProfile
from django.contrib.auth.admin import UserAdmin

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'country')


class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('username', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Account, AccountAdmin)
