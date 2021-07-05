from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin, UserManager
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.email_sender import send_multi_format_email
from core.utils import generate_code


class SlaveUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        now = timezone.now()
        extra_fields.setdefault('last_login', now)
        extra_fields.setdefault('date_joined', now)

        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_verified', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class SlaveUser(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_verified = models.BooleanField(
        _('verified'),
        default=False,
        help_text=_(
            'Designates whether this user is verified the email address.'
        )
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = SlaveUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-id']

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class SlaveUserProfile(models.Model):
    user = models.OneToOneField(SlaveUser, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="profiles/avatars/", null=True, blank=True)
    banner = models.ImageField(upload_to="profiles/banners/", null=True, blank=True)
    bio = models.TextField(blank=True)

    app_notify = models.BooleanField(default=False)
    email_notify = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('user',)
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    @receiver(post_save, sender=SlaveUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            SlaveUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=SlaveUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class AbcBaseCode(models.Model):
    EXPIRY_PERIOD = 3  # day

    user = models.ForeignKey(SlaveUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=40, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def send_mail(self, prefix):
        context = {
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'code': self.code
        }
        send_multi_format_email(prefix, context, target_email=self.user.email)

    def __str__(self):
        return self.code


class SignUpCodeManager(models.Manager):
    def create_signup_code(self, user, ip_address):
        code = generate_code()
        signup_code = self.create(
            user=user,
            code=code,
            ip_address=ip_address
        )
        return signup_code

    def set_user_is_verified(self, code):
        try:
            signup_code = SignUpCode.objects.get(code=code)
            signup_code.user.is_verified = True
            signup_code.user.save()
            return True
        except SignUpCode.DoesNotExist:
            pass
        return False


class SignUpCode(AbcBaseCode):
    ip_address = models.GenericIPAddressField()

    objects = SignUpCodeManager()

    class Meta:
        verbose_name = 'Signup Code'
        verbose_name_plural = 'Signup Codes'

    def send_signup_mail(self):
        self.send_mail(prefix='signup_email')


class PasswordResetCodeManager(models.Manager):
    def create_password_reset_code(self, user):
        code = generate_code()
        password_reset_code = self.create(
            user=user,
            code=code
        )
        return password_reset_code

    def get_expiry_period(self):
        return AbcBaseCode.EXPIRY_PERIOD


class PasswordResetCode(AbcBaseCode):
    objects = PasswordResetCodeManager()

    class Meta:
        verbose_name = 'Password Reset Code'
        verbose_name_plural = 'Password Reset Codes'

    def send_password_reset_email(self):
        self.send_mail(prefix='password_reset_email')


class EmailChangeCodeManager(models.Manager):
    def create_email_change_code(self, user, email):
        code = generate_code()
        email_change_code = self.create(
            user=user,
            code=code,
            email=email
        )

        return email_change_code

    def get_expiry_period(self):
        return AbcBaseCode.EXPIRY_PERIOD


class EmailChangeCode(AbcBaseCode):
    email = models.EmailField(max_length=255)

    objects = EmailChangeCodeManager()

    class Meta:
        verbose_name = 'Email Change Code'
        verbose_name_plural = 'Email Change Codes'

    def send_email_change_email(self):
        self.send_mail(prefix='email_change_notify_previous_email')

        prefix = 'email_change_confirm_new_email'
        context = {
            'email': self.email,
            'code': self.code
        }
        send_multi_format_email(prefix, context, target_email=self.email)


class UserFollowing(models.Model):
    user = models.ForeignKey(SlaveUser, related_name='following', on_delete=models.CASCADE)
    following_user = models.ForeignKey(SlaveUser, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        constraints = [
            models.UniqueConstraint(fields=['user', 'following_user'], name='unique_followers')
        ]

    def __str__(self):
        return f'{self.user} follows {self.following_user}'
