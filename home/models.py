from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User




# Create your models here.
class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    is_employer=models.BooleanField(default=False)
    PhoneNumber=models.CharField(max_length=50, blank=True)
    address=models.TextField()
    education=models.TextField(max_length=50, blank=True)
    profession=models.CharField(max_length=50, blank=True)
    experiance=models.TextField(max_length=50, blank=True)
    country=models.CharField(max_length=50, blank=True)
    state=models.CharField(max_length=50, blank=True)
    profile_pic=models.ImageField(upload_to="media/media",null=True,blank=True)
    

  

    def __str__(self):
        return self.user.username
    
User.userprofile = property(lambda u: Userprofile.objects.get_or_create(user=u)[0])

JOB_TYPE = (
    ('Part Time', 'Part Time'),
    ('Full Time', 'Full Time'),
    ('Freelance', 'Freelancer'),
)

CATEGORY = (
    ('Web Design', 'Web Design'),
    ('Graphic Design', 'Graphic Design'),
    ('Web Developing', 'Web Developing'),
    ('Software Engineering', 'Software Engineering'),
    ('HR', 'HR'),
    ('Marketing', 'Marketing'),
)

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Any', 'Any'),
)

class JobPosting(models.Model):
    created_by = models.ForeignKey(User,related_name='jobs', on_delete=models.CASCADE,
                        null=True ,  editable=False, blank=True)
    title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200)
    employment_status = models.CharField(choices=JOB_TYPE, max_length=10)
    vacancy = models.CharField(max_length=10, null=True)
    gender = models.CharField(choices=GENDER, max_length=30, null=True)
    category = models.CharField(choices=CATEGORY, max_length=30)
    description = models.TextField()
    responsibilities = models.TextField()
    experience = models.CharField(max_length=100)
    job_location = models.CharField(max_length=120)
    Salary = models.CharField(max_length=100, null=True, blank=True)
    application_deadline = models.DateTimeField()
    published_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-published_on']
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("job_single", args=[str(self.pk)])



class Application(models.Model):
    job = models.ForeignKey(JobPosting,related_name='applications',on_delete=models.CASCADE)
    content=models.CharField( max_length=300)
    experiance=models.CharField(max_length=300)
    created_by = models.ForeignKey(User,related_name='applications', on_delete=models.CASCADE,
                        null=True ,  editable=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.job.title

class ConversationMessage(models.Model):

    application = models.ForeignKey(Application,related_name='conversationmessages',on_delete=models.CASCADE)
    content=models.TextField()
    created_by = models.ForeignKey(User,related_name='conversationmessages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['created_at']


class Notification(models.Model):

    MESSAGE='message'
    APPLICATION='application'
    
    CHOICES =(
        (MESSAGE,'Message'),
        (APPLICATION,'Application')
    )

    to_user=models.ForeignKey(User,related_name='notifications',on_delete=models.CASCADE)
    notification_type =models.CharField(max_length=20,choices=CHOICES)
    is_read =models.BooleanField(default=False)
    extra_id= models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,related_name='creatednotifications', on_delete=models.CASCADE)
    class Meta:
        ordering=['created_at']

