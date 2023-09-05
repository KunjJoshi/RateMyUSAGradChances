from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields ):
        if not email:
            raise ValueError('Email Must be entered')
        try:
            user=self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
        except:
            raise
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(email, password, **extra_fields)
    


class User(AbstractBaseUser, PermissionsMixin):
    name=models.CharField(max_length=100, null=True, blank=True)
    username=models.CharField(max_length=100, null=True, blank=True, unique=True)
    email=models.EmailField(max_length=100, blank=True, unique=True, null=True)
    phone_regex = RegexValidator(regex = r'^(\+\d{0,13}|\s*)?$', message="Phone Number Must be entered in the Country Code Format")
    phone=models.CharField(validators=[phone_regex],max_length=100, null=True, blank=True, unique=True)
    password=models.CharField(max_length=256)
    city=models.CharField(max_length=100)
    college=models.CharField(max_length=1000)
    state=models.CharField(max_length=100)
    gre_given=models.BooleanField(default=False, null=True, blank=True)
    gre_waiveoff=models.BooleanField(default=False, null=True, blank=True)
    gre_score_quant_verbal=models.CharField(max_length=100,default='0',null=True, blank=True)
    gre_score_awa=models.CharField(max_length=100,default='0',null=True,blank=True)
    toefl_given=models.BooleanField(default=False)
    ielts_given=models.BooleanField(default=False)
    toefl_score=models.CharField(max_length=100,default='0',null=True,blank=True)
    ielts_bands=models.CharField(max_length=100,default='0',null=True, blank=True)
    noofprojects=models.CharField(max_length=100,default='0',null=True, blank=True)
    has_relevant_work_ex=models.CharField(max_length=100,default=False,null=True, blank=True)
    work_ex_years=models.CharField(max_length=100,default='0',null=True, blank=True)
    noof_research_papers=models.CharField(max_length=100,default='0',null=True,blank=True)
    noof_patents=models.CharField(max_length=100,default='0',blank=True, null=True)
    noof_conference_papers=models.CharField(max_length=100,default='0',blank=True, null=True)
    grade=models.CharField(max_length=100,default='0',null=True, blank=True)
    max_possible_grade=models.CharField(max_length=100,default='10',null=True, blank=True)
    profile_score=models.CharField(max_length=100,default='0',blank=True, null=True)
    is_staff=models.BooleanField(default=False, null=True, blank=True)
    is_superuser=models.BooleanField(default=False, null=True, blank=True)
    backlogs_in_first_two_sems=models.CharField(max_length=3,default='0',null=True, blank=True)
    backlogs_in_rest=models.CharField(max_length=3, default='0',null=True, blank=True)
    noof_relevant_courses=models.CharField(max_length=4, default='0', null=True, blank=True)
    objects=UserManager()

    USERNAME_FIELD='email'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


    class Meta:
        verbose_name='User'
    
    def __str__(self):
        return self.email

class Otp(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    otp=models.CharField(max_length=256, null=True, blank=True)
    otp_date=models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name='OTP'
class Universities(models.Model):
    uni_name=models.CharField(max_length=1000, blank=True, null=True)
    uni_code=models.CharField(max_length=5, blank=True, null=True)
    course=models.CharField(max_length=1000, null=True, blank=True)
    picture=models.CharField(max_length=1000, null=True, blank=True)
    preferred_profile_score=models.CharField(max_length=100,default='0',blank=True, null=True)
    location=models.CharField(max_length=100, blank=True, null=True)
    world_ranking=models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        verbose_name='Universitie'
    
    def __str__(self):
        return self.uni_name



