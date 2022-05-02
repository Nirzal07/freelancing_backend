from django.contrib import admin
from django.contrib.admin.decorators import display
from django.contrib.auth.models import Group

from .models import User, ClientAccount, FreelancerAccount, VerificationCode, Portfolio
from rest_framework.authtoken.models import Token
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
admin.site.empty_value_display = '(Empty)'


class TokenInline(admin.StackedInline):
    model = Token
class ClientAccountInline(admin.StackedInline):
    model = ClientAccount

class FreelancerAccountInline(admin.StackedInline):
    model = FreelancerAccount

class UserAdmin(BaseUserAdmin):
    model = User
    # inlines = [
    #     ClientAccountInline,
    #     FreelancerAccountInline,
    #     TokenInline
    #            ]
    list_display = ('id', 'email','is_freelancer')
    list_display_links = ('id', 'email','is_freelancer')
    list_filter = ('email', 'is_freelancer')
    fieldsets = (
        (None, {'fields': ('is_freelancer', 'is_verified', 'email', 'password', 'auth_provider')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('is_freelancer', 'is_verified', 'email', 'auth_provider', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    list_filter = ('is_freelancer',)
    inlines = [
        TokenInline,
        ClientAccountInline,
        FreelancerAccountInline,
        
    ]

admin.site.register(User, UserAdmin)

class UserInline(admin.TabularInline):
    model = User


@admin.register(FreelancerAccount)
class FreelancerAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'contact']
    list_display_links = ['id', 'full_name', 'contact']
    ordering = ()
    search_fields = ('email',) 
    # add acounts in readonly fields
    readonly_fields =('registered_date',)
    list_filter = ('gender',)

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['id', 'freelancer', 'title']
    list_display_links =['id', 'freelancer', 'title']
    ordering = ("created_date",)
    search_fields = ('freelancer', 'title',) 
    readonly_fields =('created_date',"updated_date")


# @admin.register(VerificationCode)
# class VCAdmin(admin.ModelAdmin):
#     pass

@admin.register(ClientAccount)
class ClientAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name']
    list_display_links = ['id', 'full_name']
    ordering = ()
    readonly_fields =('registered_date',)
    search_fields = ('email',) 


# remove Group from admin panel
admin.site.unregister(Group)