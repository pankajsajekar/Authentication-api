import random
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

# Third-Party Library Imports
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.
# class Register(models.Model):
#     name = models.CharField(max_length=200)
#     email = models.CharField(max_length=200, unique=True)
#     password = models.CharField(max_length=200)
#     mobile = models.IntegerField()
#     register_id = models.CharField(max_length=100, blank=True, unique=True, editable=True)

#     def save(self, *args, **kwargs):
#         self.register_id = "ST" + str(random.randint(100000, 999999))
#         return super().save(*args, **kwargs)


# custome user manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile, password=None, password2=None, is_candidate=None, is_employer=None):
        """
        Creates and saves a User with the given email,name, mobile, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name = name,
            mobile = mobile,
            is_candidate = is_candidate,
            is_employer = is_employer,
        )

        user.set_password(password)
        user.save(using=self._db)
        print("user is created")
        return user

    def create_superuser(self, email, name, mobile, password=None, **other_fields):
        print("start creating superuser")
        """
        Creates and saves a superuser with the given email,name, mobile, and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            mobile=mobile,
            is_candidate=False,
            is_employer=False
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mobile = PhoneNumberField(_("mobile number"), unique=False, blank=False, default="+91818053481")
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True, )
    name = models.CharField(max_length=200)
    register_id = models.CharField(max_length=100, blank=True, unique=True, editable=True)
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_candidate = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile']

    def save(self, *args, **kwargs):
        self.register_id = "ST" + str(random.randint(100000, 999999))
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class CandidateModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="candidateModel")
    first_name = models.CharField(max_length=75, blank=True, null=True)
    last_name = models.CharField(max_length=75, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, default="2001/01/01")
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True)
    city = models.CharField(max_length=75, blank=True)
    state = models.CharField(max_length=75, blank=True)
    country = models.CharField(max_length=75, blank=True)

    # Custom functrions to get name, full name and birth date.
    def get_fullName(self):
        return f"{self.first_name} {self.last_name}"

    def get_shortName(self):
        return f"{self.first_name}"

    def get_birth_date(self):
        return f"{self.date_of_birth}"

    # Its a child class to change the meta data of the User model
    # verbose_name_plural is used to name the plural form of User
    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class EmployerModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employerModel")
    company_name = models.CharField(max_length=255)
    company = 'company'
    consultant = 'consultant'
    company_type_choices = (
        (company, company),
        (consultant, consultant)
    )
    company_type = models.CharField(max_length=25, choices=company_type_choices, default=company)
    gst_in = models.CharField(max_length=100, blank=True )
    designation = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=75, blank=True)
    state = models.CharField(max_length=75, blank=True)
    country = models.CharField(max_length=75, blank=True)

    def __str__(self):
        return self.company_name

class AdminProfileModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="admin_profiles")
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    date_of_birth = models.DateField(blank=True)
    age = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=75, blank=True)
    state = models.CharField(max_length=75, blank=True)
    country = models.CharField(max_length=75, blank=True)

    # Custom functrions to get name, full name and birth date.

    def get_fullName(self):
        return f"{self.first_name} {self.last_name}"

    def get_shortName(self):
        return f"{self.first_name}"

    def get_birth_date(self):
        return f"{self.date_of_birth}"

    # Its a child class to change the meta data of the User model
    # verbose_name_plural is used to name the plural form of User

    class Meta:
        verbose_name = "Admin Profile"
        verbose_name_plural = "Admin Profiles"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"