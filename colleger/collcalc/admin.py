from django.contrib import admin
from .models import *
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'email', 'phone', 'college','profile_score', )
admin.site.register(User,StudentAdmin)

class UniversityAdmin(admin.ModelAdmin):
    list_display=('uni_name','uni_code','world_ranking',)
admin.site.register(Universities,UniversityAdmin)

class OtpAdmin(admin.ModelAdmin):
    list_display=('user','otp',)
admin.site.register(Otp, OtpAdmin)