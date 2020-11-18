from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout

from home.models import JobPosting ,Application ,ConversationMessage
from django.shortcuts import render, redirect  , get_object_or_404
from .forms import EmployeeForm, ApplicationForm
from .models import JobPosting ,Userprofile ,Notification
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.utilities import create_notification
from django.views.generic import  ListView
from django.db.models import Q


# Create your views here.
def index(request):
    jobs=JobPosting.objects.all()
   
    if request.user.is_anonymous :
       
        return redirect('/login')
       
        
    return render(request,'index.html',{'jobs':jobs,
                      'userprofile':request.user.userprofile  })

def loginUser(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            
            login(request,user)
            return redirect("/")
            
            # A backend authenticated the credentials
         
        else:
             # No backend authenticated the credentials
            messages.error(request, "Invalid username or password!")
            return render(request,'login.html')

    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return render(request,'login.html')
def register(request):
       if request.method == 'POST':
           first_name=request.POST["first_name"]
           last_name=request.POST["last_name"]
           username=request.POST["username"]
           email=request.POST["email"]
          
           password=request.POST["password"]
           confirm_password=request.POST["confirm_password"]
           user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
           
           account_type= request.POST.get('account_type','jobseeker')
           if account_type == 'employer':
               userprofile=Userprofile.objects.create(user=user,is_employer=True)
               userprofile.save()
           else:
               userprofile=Userprofile.objects.create(user=user)
               userprofile.save()
           return redirect('/login')
       else:  
           return render(request,'register.html')    

# Create your views here.

def post(request):  
    if request.method == "POST":  
        form = EmployeeForm(request.POST)  
        if form.is_valid():  
            try:  
                job=form.save()
                job.created_by = request.user
                job.save()  
                return redirect('/')  
            except:  
                pass  
    else:  
        form = EmployeeForm()  
    return render(request,'jpost.html')
def job_single(request, pk):
    
    q = JobPosting.objects.get(id=pk)
    context={'q':q,
              'userprofile':request.user.userprofile}
    return render(request, "job_single.html",context)
@login_required
def profile(request):
      userdetails=Userprofile.objects.all()
      context={'userprofile':request.user.userprofile}
     
      return render(request,"profile.html",context)

@login_required
def apply_for_job(request,pk):
    job=JobPosting.objects.get(id=pk)

    if request.method == 'POST':
         form= ApplicationForm(request.POST)     

         if form.is_valid():
             application=form.save(commit=False)
             application.job=job
             application.created_by=request.user
             application.save()
             create_notification(request , to_user=job.created_by ,notification_type='application', extra_id=application.id)
            
             return redirect("/profile")
    else:
             form=ApplicationForm()

    return render(request,'application.html',{'form':form,'job':job})
@login_required

def view_application(request,app_id):
    if request.user.userprofile.is_employer:
        application = get_object_or_404(Application, pk= app_id, job__created_by= request.user)
    else:
        application = get_object_or_404(Application, pk= app_id, created_by= request.user)
    if request.method== "POST":
        content= request.POST.get('content') 
        if content:
            conversationmessage= ConversationMessage.objects.create(application=application,content=content, created_by= request.user)
            create_notification(request , to_user=application.created_by ,notification_type='message', extra_id=application.id)
            return redirect ('view_application',app_id=app_id)   
    return render(request,'viewapplication.html',{'application':application})


def view_postedjob(request,id):
    job=get_object_or_404(JobPosting,pk=id, created_by=request.user)

    return render (request,"postedjob.html",{'job':job})

@login_required
def notification(request):
    goto= request.GET.get('goto','')
    notification_id=request.GET.get('notification',0)
    extra_id =request.GET.get('extra_id',0) 
    if goto !='':
        notification=Notification.objects.get(pk=notification_id)
        notification.is_read=True
        notification.save()

        if notification.notification_type == Notification.MESSAGE:
            return redirect('view_application',app_id=notification.extra_id)
        elif notification.notification_type == Notification.APPLICATION:
            return redirect('view_application',app_id=notification.extra_id) 
    return render(request,'notification.html')


class SearchResultsView(ListView):
    model = JobPosting
    template_name = 'search_results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('title','job_location')
        object_list = JobPosting.objects.filter(
            Q(title__icontains=query) | Q(job_location__icontains=query)  | Q(employment_status__icontains=query)
        )
        return object_list
        return query
