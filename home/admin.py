from django.contrib import admin
from .models import Application
from .models import JobPosting,Userprofile
from django.http import request

# Register your models here.
class JobAdmin(admin.ModelAdmin):
    
    list_display=('title','company_name','job_location','Salary','created_by')
   
admin.site.register(JobPosting,JobAdmin)
admin.site.register(Userprofile)
admin.site.register(Application)

