from django.contrib import admin
from .models import userarea
from .models import JobPosting
from django.http import request

# Register your models here.
class JobAdmin(admin.ModelAdmin):
    
    list_display=('title','company_name','job_location','Salary','author')
    def save_model(self, request, obj, form, change):
        obj.created_user=request.user
        obj.save()
   
        
            
        
   
admin.site.register(userarea)
admin.site.register(JobPosting,JobAdmin)

