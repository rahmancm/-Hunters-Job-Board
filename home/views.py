from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from .models import userarea
from home.models import JobPosting
from django.shortcuts import render, redirect  , get_object_or_404
from .forms import EmployeeForm  
from .models import JobPosting  
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    jobs=JobPosting.objects.all()
 
    if request.user.is_anonymous :
       
        return redirect('/login')
       
        
    return render(request,'index.html',{'jobs':jobs,
                        })

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
           user=User.objects.create(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
           user.save()
           print("User created")
           return redirect('/login')
       else:  
           return render(request,'register.html')    

# Create your views here.

def post(request):  
    if request.method == "POST":  
        form = EmployeeForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/')  
            except:  
                pass  
    else:  
        form = EmployeeForm()  
    return render(request,'jpost.html')
def job_single(request, pk):
    
    q = JobPosting.objects.get(id=pk)
    context={'q':q
              }
    return render(request, "job_single.html",context)

def profile(request):
     if request.user.is_anonymous :
           
        return redirect('/login')
     return render(request,"profile.html")