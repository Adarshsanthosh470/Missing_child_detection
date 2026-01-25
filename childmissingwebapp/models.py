from django.db import models

# Create your models here.
class register(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=20)
    phone=models.IntegerField()


from django.db import models

class NewCase(models.Model):
    # Define Gender choices
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    # Define Status choices
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]
    
    childname = models.CharField(max_length=25)
    dob = models.DateField()  # Added parentheses
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        default='other',
    )
    height = models.PositiveIntegerField()  # in cm
    weight = models.PositiveIntegerField()  # in kg
    eye_color = models.CharField(max_length=50)
    hair_color = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='missing_children_photos/', blank=True, null=True)
    last_seen_date = models.DateTimeField() 
    last_seen_location = models.CharField(max_length=255) 

    # Parent/Guardian Information
    guardian_name = models.CharField(max_length=255) 
    guardian_phone = models.CharField(max_length=15) 
    guardian_email = models.EmailField() 

    # Possible Suspects
    suspect_name = models.CharField(max_length=255, blank=True, null=True)  
    suspect_description = models.TextField(blank=True, null=True) 
    vehicle_info = models.CharField(max_length=255, blank=True, null=True)  

    # Search Efforts
    authorities_contacted = models.BooleanField(default=False) 
    search_efforts = models.TextField(blank=True, null=True) 

    # Case Status
    status = models.CharField(
        max_length=7,  # 'active' or 'closed'
        choices=STATUS_CHOICES,
        default='active',  # Default is active
    )

    def __str__(self):
        return self.childname


from django.db import models

class ChildLocator(models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=6, choices=gender_choices)
    image = models.ImageField(upload_to='child_locator_images/')
    height_cm = models.PositiveIntegerField(blank=True, null=True)
    weight_kg = models.PositiveIntegerField(blank=True, null=True)
    hair_color_choices = [
        ('black', 'Black'),
        ('brown', 'Brown'),
        ('blonde', 'Blonde'),
        ('red', 'Red'),
        ('grey', 'Grey'),
    ]
    hair_color = models.CharField(max_length=6, choices=hair_color_choices, blank=True, null=True)
    distinctive_marks = models.TextField(blank=True, null=True)
    last_seen_location = models.CharField(max_length=255)
    last_seen_date = models.DateField()
    last_known_clothing = models.TextField(blank=True, null=True)

    guardian_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    email= models.EmailField(blank=True, null=True)
    accept = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Child Locator Report for {self.full_name}"
    
from django.db import models

class Feedback(models.Model):
    user = models.ForeignKey(register,on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField()

from django.db import models

class ChildRecoveryCase(models.Model):
    childloc = models.ForeignKey(ChildLocator,on_delete=models.CASCADE, null=True, blank=True)
    case = models.ForeignKey(NewCase,on_delete=models.CASCADE, null=True, blank=True)
    date_disappearance = models.DateField()
    description = models.TextField()
    suspected_causes = models.CharField(max_length=255, blank=True, null=True)
    who_involved = models.CharField(max_length=255, blank=True, null=True)
    tools_methods = models.CharField(max_length=255, blank=True, null=True)
    found_location = models.TextField()
    who_found = models.CharField(max_length=255, blank=True, null=True)
    recovery_wellbeing = models.TextField(blank=True, null=True)
    legal_actions = models.TextField(blank=True, null=True)
    submitted_by = models.CharField(max_length=255)

    def __str__(self):
        return f"Case {self.case_id} - {self.child_name}"
    



from django.db import models

class VideoScan(models.Model):
    video = models.FileField(upload_to="uploaded_videos/")
    matched_child = models.CharField(max_length=100, blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)



from django.db import models


class SocialPost(models.Model):
    user_name = models.CharField(max_length=200)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to="social_posts/")
    created_at = models.DateTimeField(auto_now_add=True)

