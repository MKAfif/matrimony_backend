from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,Permission,Group
from django.utils.translation import gettext_lazy as _
from .manager import UserManager

class Member(models.Model):
    gender_choice = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    matrimony_id              =   models.CharField(unique=True, max_length=10)
    matrimony_profile_for     =   models.CharField(max_length=255)  
    gender                    =   models.CharField(choices=gender_choice, max_length=6) 
    name                      =   models.CharField(max_length=255)  
    mobile_number             =   models.CharField(max_length=10)


class Basic_Details(AbstractBaseUser,PermissionsMixin):
    member               =   models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True, related_name='basic_details_profile')
    date_of_birth        =   models.DateField()
    religion             =   models.CharField(max_length=30)
    mother_tongue        =   models.CharField(max_length=30)
    email_id             =   models.EmailField(unique=True)
    is_staff             =   models.BooleanField(default=False)
    is_superuser         =   models.BooleanField(default=False)
    is_active            =   models.BooleanField(default=False)
    is_verified          =   models.BooleanField(default=False)
   
    objects = UserManager()
   
    USERNAME_FIELD = 'email_id'
    REQUIRED_FIELDS = []
   
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='basic_details_user_permissions' 
    )
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='basic_details_groups' 
    )

class Personal_Details(models.Model):
    marital_status_choices = (
         ('Never Married', 'Never Married'),
        ('Married', 'Married'),
    )

    family_status_choices = (
       ('Upper Middle Class', 'Upper Middle Class'),
        ('Middle Class', 'Middle Class'),
        ('Rich', 'Rich')
    )

    family_type_choices = (
        ('Joint', 'Joint'),
        ('Nuclear', 'Nuclear'),
    )

    family_values_choices = (
        ('Orthodox', 'Orthodox'),
        ('Traditional', 'Traditional'),
        ('Moderate', 'Moderate'),
        ('Liberal', 'Liberal'),
        
    )

    member                   =  models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True, related_name='personal_details_profile')
    marital_status           =  models.CharField(max_length=15, choices=marital_status_choices)
    height                   =  models.CharField(max_length=20)
    family_status            =  models.CharField(max_length=30, choices=family_status_choices)
    family_type              =  models.CharField(max_length=30, choices=family_type_choices)
    family_values            =  models.CharField(max_length=30, choices=family_values_choices)


class Professional_Details(models.Model):
    employed_in_choices = (
        ('Government', 'Government'),
        ('Private', 'Private'),
        ('Business', 'Business'),
        ('Defence', 'Defence'),
        ('Self Employed', 'Self Employed'),
        ('Not Working', 'Not Working'),
    )

    INCOME_CHOICES = (
        ('below_1_lakh', 'Below 1 lakh'),
        ('1 - 2 lakh', '1 - 2 lakh'),
        ('2 - 3 lakh', '2 - 3 lakh'),
        ('3 - 4 lakh', '3 - 4 lakh'),
        ('4 - 5 lakh', '4 - 5 lakh'),
        ('5 - 6 lakh', '5 - 6 lakh'),
        ('6 - 7 lakh', '6 - 7 lakh'),
        ('7 - 8 lakh', '7 - 8 lakh'),
        ('8 - 9 lakh', '8 - 9 lakh'),
        ('9 - 10 lakh', '9 - 10 lakh'),
        ('Above 10 lakh', 'Above 10 lakh'),
    )

    member              =    models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True, related_name='professional_details_profile')
    highest_education   =    models.CharField(max_length=50)
    employed_in         =    models.CharField(max_length=30, choices=employed_in_choices)
    annual_income       =    models.CharField(max_length=30, choices=INCOME_CHOICES)
    work_location       =    models.CharField(max_length=30)
    state               =    models.CharField(max_length=30)
    occupation          =    models.CharField(max_length=30 , null= True)

class About(models.Model):
    member        =  models.OneToOneField(Member, on_delete=models.CASCADE, null=True, blank=True, related_name='about_profile')
    about_you     =  models.CharField(max_length=200)


class Image(models.Model):

    member              =    models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True, related_name='image')
    image               =    models.ImageField()


class Preferences (models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True, related_name='preferences')
    age_range_min = models.IntegerField()
    age_range_max = models.IntegerField()
    location = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    height = models.CharField(max_length=20)
    eye_color = models.CharField(max_length=20)  
    skin_tone = models.CharField(max_length=20) 
    body_type = models.CharField(max_length=20)  
    hobbies = models.CharField(max_length=200)

    def __str__(self):
        return f"Preferences for {self.member}"
    
class MembershipPackage(models.Model):
    plan_name   = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    plan_price  = models.DecimalField(max_digits=10, decimal_places=2)
    time_period = models.PositiveIntegerField()