from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from account import models, forms


@admin.register(models.SignUpCode)
class SignUpCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'ip_address', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('user', 'code', 'ip_address')

    def has_add_permission(self, request):
        return False


class SignUpCodeInline(admin.TabularInline):
    model = models.SignUpCode
    fieldsets = (
        (None, {
            'fields': ('code', 'ip_address', 'created_at')
        }),
    )
    readonly_fields = ('code', 'ip_address', 'created_at')
    extra = 0


@admin.register(models.PasswordResetCode)
class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('user', 'code')

    def has_add_permission(self, request):
        return False


class PasswordResetCodeInline(admin.TabularInline):
    model = models.PasswordResetCode
    fieldsets = (
        (None, {
            'fields': ('code', 'created_at')
        }),
    )
    readonly_fields = ('code', 'created_at')
    extra = 0


@admin.register(models.EmailChangeCode)
class EmailChangeCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'email', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('user', 'code', 'email')

    def has_add_permission(self, request):
        return False


class EmailChangeCodeInline(admin.TabularInline):
    model = models.EmailChangeCode
    fieldsets = (
        (None, {
            'fields': ('code', 'email', 'created_at')
        }),
    )
    readonly_fields = ('code', 'email', 'created_at')
    extra = 0


class ProfileInline(admin.StackedInline):
    model = models.SlaveUserProfile
    can_delete = False
    fieldsets = (
        (None, {
            'fields': ('avatar', 'banner', 'bio', 'app_notify', 'email_notify')
        }),
        # ("Social Links", {
        #     'fields': ('social_facebook', 'social_twitter', 'social_instagram', 'social_pinterest')
        # })
    )


@admin.register(get_user_model())
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('username', 'first_name', 'last_name', 'is_verified')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    # form = forms.UserUpdateForm
    # add_form = forms.UserCreationForm
    inlines = [ProfileInline, SignUpCodeInline, PasswordResetCodeInline, EmailChangeCodeInline]
    list_display = ('email', 'is_verified', 'first_name', 'last_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    ordering = ('email',)
    readonly_fields = ('is_verified',)
