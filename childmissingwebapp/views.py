from django.shortcuts import render, HttpResponse,redirect
from .import models
# Create your views here.

def index1(request):
    return render(request,'index1.html')

def home1(request):
    return render(request,'home1.html')

def register(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        if models.register.objects.filter(email=email).exists():
            alert="<script> alert('email already exist'); window.location.href='/register/'; </script>"
            return HttpResponse(alert)
        try:
            newuser=models.register(name=name,password=password,email=email,phone=phone)
            newuser.save()
            return redirect('login')
        except Exception as e:
            alert="<script> alert('Error'); window.location.href='/register/'; </script>"
            return HttpResponse(alert)
    else:
        return render(request,'register.html')

def login(request):
    if request.method =='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        if models.register.objects.filter(email=email,password=password).exists():
         request.session['email']=email
         return redirect('home1')
        else:
            alert="<script> alert('Login Failed'); window.location.href='/index1/'; </script>"
            return HttpResponse(alert)
    else:
        return render(request,'login.html')    
    
def profile(request):
    if 'email' in request.session:
        email=request.session['email']
        data=models.register.objects.get(email=email)
        return render(request,'profile.html',{'data':data})
    else:
        return redirect('login')

def logout(request):
    request.session.flush()
    return redirect('index')

def update(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            user = models.register.objects.get(email=email)
            if request.method == 'POST': 
                user.name = request.POST.get('name')
                user.password = request.POST.get('password')
                user.phone = request.POST.get('phone')
                user.save() 
                return redirect('profile')  # Redirect to profile page
            return render(request, 'update.html', {'user': user})  # Render the form
        except models.register.DoesNotExist:  # Handle the case where the user does not exist
            alert = "<script>alert('User not found. Please log in again.');window.location.href='/login/';</script>"
            return HttpResponse(alert)
    else:  # Handle case where user is not logged in
        return redirect('login')

def adminhome(request):
    cases = NewCase.objects.all()
    u=models.register.objects.count()
    c=models.NewCase.objects.count()
    o=models.Feedback.objects.count()
    return render(request, 'adminhome.html', {'cases': cases,'u':u,'c':c,'o':o,})

def NewCase_list(request):
    new_cases = NewCase.objects.all()  # Fetch NewCase records
    child_locators = ChildLocator.objects.all()  # Fetch ChildLocator records
    return render(request, 'NewCase_list.html', {'new_cases': new_cases, 'child_locators': child_locators})

from django.shortcuts import render, redirect
from .models import NewCase, ChildLocator
def deletecase(request, uid, model_type):
    if model_type == 'newcase':
        case = NewCase.objects.get(id=uid)
        case.delete()
    elif model_type == 'childlocator':

        locator = ChildLocator.objects.get(id=uid)
        locator.delete()
    if model_type == 'newcase':
        return redirect('NewCase_list') 
    else:
        return redirect('NewCase_list') 


def adminlog(request):
    if request.method =='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        e='admin@gmail.com'
        p='admin'
        if email==e:
            if password==p:
                request.session['email']=email
                return redirect('adminhome')
    else:
        return render(request,'adminlog.html')

def userlist(request):
    user=models.register.objects.all()
    return render(request,'userlist.html',{'user':user})


def deleteuser(request,uid):
    u=models.register.objects.get(id=uid)
    u.delete()
    return redirect('userlist')  
           
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import NewCase  # Import the correct model class

# def newcase(request):
#     if request.method == 'POST':
#         # Get data from the form
#         childname = request.POST.get('childname')
#         dob = request.POST.get('dob')
#         gender = request.POST.get('gender')
#         height = request.POST.get('height')
#         weight = request.POST.get('weight')
#         eye_color = request.POST.get('eye_color')
#         hair_color = request.POST.get('hair_color')
#         photo = request.FILES.get('photo') 
#         last_seen_date = request.POST.get('last_seen_date')
#         last_seen_location = request.POST.get('last_seen_location')
#         guardian_name = request.POST.get('guardian_name')
#         guardian_phone = request.POST.get('guardian_phone')
#         guardian_email = request.POST.get('guardian_email')
#         suspect_name = request.POST.get('suspect_name')
#         suspect_description = request.POST.get('suspect_description')
#         vehicle_info = request.POST.get('vehicle_info')
#         authorities_contacted = request.POST.get('authorities_contacted') == 'on'  # Handle checkbox
#         search_efforts = request.POST.get('search_efforts')
#         status = request.POST.get('status')
        
#         try:
#             # Create and save the new case
#             case = NewCase(
#                 childname=childname,
#                 dob=dob,
#                 gender=gender,
#                 height=height,
#                 weight=weight,
#                 eye_color=eye_color,
#                 hair_color=hair_color,
#                 photo=photo,
#                 last_seen_date=last_seen_date,
#                 last_seen_location=last_seen_location,
#                 guardian_name=guardian_name,
#                 guardian_phone=guardian_phone,
#                 guardian_email=guardian_email,
#                 suspect_name=suspect_name,
#                 suspect_description=suspect_description,
#                 vehicle_info=vehicle_info,
#                 authorities_contacted=authorities_contacted,
#                 search_efforts=search_efforts,
#                 status=status
#             )
#             case.save()  # Save the case to the database
            
#             # Success message
#             alert = "<script>alert('Case Submitted.');window.location.href='/adminhome/';</script>"
#             return HttpResponse(alert)
#         except Exception as e:
#             # If there's an error during saving
#             alert = f"<script>alert('Error: {str(e)}');window.location.href='/newcase/';</script>"
#             return HttpResponse(alert)
#     else:
#         return render(request, 'newcase.html')

from django.core.mail import send_mail
from django.conf import settings

def newcase(request):
    if request.method == 'POST':
        # Get data from the form
        childname = request.POST.get('childname')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        eye_color = request.POST.get('eye_color')
        hair_color = request.POST.get('hair_color')
        photo = request.FILES.get('photo') 
        last_seen_date = request.POST.get('last_seen_date')
        last_seen_location = request.POST.get('last_seen_location')
        guardian_name = request.POST.get('guardian_name')
        guardian_phone = request.POST.get('guardian_phone')
        guardian_email = request.POST.get('guardian_email')
        suspect_name = request.POST.get('suspect_name')
        suspect_description = request.POST.get('suspect_description')
        vehicle_info = request.POST.get('vehicle_info')
        authorities_contacted = request.POST.get('authorities_contacted') == 'on'  # Handle checkbox
        search_efforts = request.POST.get('search_efforts')
        status = request.POST.get('status')
        
        try:
            # Create and save the new case
            case = NewCase(
                childname=childname,
                dob=dob,
                gender=gender,
                height=height,
                weight=weight,
                eye_color=eye_color,
                hair_color=hair_color,
                photo=photo,
                last_seen_date=last_seen_date,
                last_seen_location=last_seen_location,
                guardian_name=guardian_name,
                guardian_phone=guardian_phone,
                guardian_email=guardian_email,
                suspect_name=suspect_name,
                suspect_description=suspect_description,
                vehicle_info=vehicle_info,
                authorities_contacted=authorities_contacted,
                search_efforts=search_efforts,
                status=status
            )
            case.save()  # Save the case to the database
            
            # Send notification email to all registered users
            notify_all_users(case)
            
            # Success message
            alert = "<script>alert('Case Submitted.');window.location.href='/adminhome/';</script>"
            return HttpResponse(alert)
        except Exception as e:
            # If there's an error during saving
            alert = f"<script>alert('Error: {str(e)}');window.location.href='/newcase/';</script>"
            return HttpResponse(alert)
    else:
        return render(request, 'newcase.html')

def notify_all_users(case):
    """Send email notification to all registered users about the new missing child case."""
    try:
        # Get all registered users
        all_users = models.register.objects.all()
        
        # Calculate age from date of birth
        age = calculate_age(case.dob)
        
        # Prepare email content
        subject = f"URGENT: Missing Child Alert - {case.childname}"
        
        message = f"""
MISSING CHILD ALERT

Name: {case.childname}
Age: {age}
Gender: {case.gender}
Physical Description:
- Height: {case.height}
- Weight: {case.weight}
- Eye Color: {case.eye_color}
- Hair Color: {case.hair_color}

Last Seen: {case.last_seen_date} at {case.last_seen_location}

Guardian Contact:
Name: {case.guardian_name}
Phone: {case.guardian_phone}
Email: {case.guardian_email}

"""
        # Add suspect information if available
        if case.suspect_name or case.suspect_description:
            message += f"""
Suspect Information:
Name: {case.suspect_name if case.suspect_name else 'Unknown'}
Description: {case.suspect_description if case.suspect_description else 'Not provided'}
"""

        # Add vehicle information if available
        if case.vehicle_info:
            message += f"Vehicle Information: {case.vehicle_info}\n"
            
        message += f"""
Current Status: {case.status}

If you have any information about this child, please contact the guardian immediately 
or your local authorities.

This is an automated message. Please do not reply to this email.
"""
        
        # Get sender email from settings
        from_email = settings.EMAIL_HOST_USER
        
        # Send email to each registered user in batches
        recipient_list = [user.email for user in all_users]
        
        # Send emails in batches to avoid timeout issues
        batch_size = 50
        for i in range(0, len(recipient_list), batch_size):
            batch = recipient_list[i:i+batch_size]
            send_mail(subject, message, from_email, batch, fail_silently=True)
            
    except Exception as e:
        # Log the error but don't stop the case submission
        print(f"Error sending notification emails: {str(e)}")

def calculate_age(birth_date_str):
    """Calculate age from birth date string."""
    from datetime import datetime
    try:
        # Assuming date format is YYYY-MM-DD
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return f"{age} years"
    except:
        return "Unknown"
    
def caselist(request):
    case=models.NewCase.objects.all()
    return render(request,'caselist.html',{'case':case})
    

from django.shortcuts import render
from .models import NewCase, ChildLocator
from django.db.models import Q  # Import Q for advanced filtering

def listcase(request):
    search_query = request.GET.get('search', '')

    accepted_cases = ChildLocator.objects.filter(accept=True)
    new_cases = NewCase.objects.all()

    if search_query:
        accepted_cases = accepted_cases.filter(
            Q(full_name__icontains=search_query) |
            Q(last_seen_location__icontains=search_query)
        )
        new_cases = new_cases.filter(
            Q(childname__icontains=search_query) |
            Q(last_seen_location__icontains=search_query)
        )

    return render(request, 'listcase.html', {
        'accepted_cases': accepted_cases,
        'new_cases': new_cases,
        'search_query': search_query
    })


from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.core.files.storage import default_storage
from urllib.parse import urlencode
from .models import ChildLocator

# def reportcase(request):
#     step = int(request.GET.get('step', 1))  # Get the current step, default to step 1

#     if request.method == 'POST':
#         data = request.session.get('child_locator_data', {})

#         # Step 1: Basic Information
#         if step == 1:
#             full_name = request.POST.get('full_name')
#             date_of_birth = request.POST.get('date_of_birth')
#             gender = request.POST.get('gender')
#             image = request.FILES.get('image')

#             data.update({
#                 'full_name': full_name,
#                 'date_of_birth': date_of_birth,
#                 'gender': gender,
#             })
#             request.session['child_locator_data'] = data

#             # Save image temporarily and store the path in session
#             if image:
#                 image_path = default_storage.save(f'child_locator_images/{image.name}', image)
#                 request.session['child_locator_image'] = image_path  # Store path, not file object

#             return redirect(f"{reverse('reportcase')}?{urlencode({'step': 2})}")

#         # Step 2: Physical Description
#         elif step == 2:
#             height_cm = request.POST.get('height_cm')
#             weight_kg = request.POST.get('weight_kg')
#             hair_color = request.POST.get('hair_color')
#             distinctive_marks = request.POST.get('distinctive_marks', '')

#             data.update({
#                 'height_cm': height_cm,
#                 'weight_kg': weight_kg,
#                 'hair_color': hair_color,
#                 'distinctive_marks': distinctive_marks,
#             })
#             request.session['child_locator_data'] = data

#             return redirect(f"{reverse('reportcase')}?{urlencode({'step': 3})}")

#         # Step 3: Last Known Location
#         elif step == 3:
#             last_seen_location = request.POST.get('last_seen_location')
#             last_seen_date = request.POST.get('last_seen_date')
#             last_known_clothing = request.POST.get('last_known_clothing', '')

#             data.update({
#                 'last_seen_location': last_seen_location,
#                 'last_seen_date': last_seen_date,
#                 'last_known_clothing': last_known_clothing,
#             })
#             request.session['child_locator_data'] = data

#             return redirect(f"{reverse('reportcase')}?{urlencode({'step': 4})}")

#         # Step 4: Contact Information & Save Data
#         elif step == 4:
#             guardian_name = request.POST.get('guardian_name')
#             contact_number = request.POST.get('contact_number')
#             email = request.POST.get('email')

#             data.update({
#                 'guardian_name': guardian_name,
#                 'contact_number': contact_number,
#                 'email': email
#             })

#             # Retrieve stored image path
#             image_path = request.session.pop('child_locator_image', None)

#             # Save to database
#             case = ChildLocator.objects.create(**data)

#             if image_path:
#                 case.image.name = image_path  # Assign stored image path to model
#                 case.save()

#             # Clear session data
#             request.session.pop('child_locator_data', None)

#             return HttpResponse("<script>alert('Case Submitted. Under Verification'); window.location.href='/home1/';</script>")

#     return render(request, 'reportcase.html', {'step': step})

from django.core.mail import send_mail
from django.conf import settings

def reportcase(request):
    step = int(request.GET.get('step', 1))  # Get the current step, default to step 1

    if request.method == 'POST':
        data = request.session.get('child_locator_data', {})

        # Step 1: Basic Information
        if step == 1:
            full_name = request.POST.get('full_name')
            date_of_birth = request.POST.get('date_of_birth')
            gender = request.POST.get('gender')
            image = request.FILES.get('image')

            data.update({
                'full_name': full_name,
                'date_of_birth': date_of_birth,
                'gender': gender,
            })
            request.session['child_locator_data'] = data

            # Save image temporarily and store the path in session
            if image:
                image_path = default_storage.save(f'child_locator_images/{image.name}', image)
                request.session['child_locator_image'] = image_path  # Store path, not file object

            return redirect(f"{reverse('reportcase')}?{urlencode({'step': 2})}")

        # Step 2: Physical Description
        elif step == 2:
            height_cm = request.POST.get('height_cm')
            weight_kg = request.POST.get('weight_kg')
            hair_color = request.POST.get('hair_color')
            distinctive_marks = request.POST.get('distinctive_marks', '')

            data.update({
                'height_cm': height_cm,
                'weight_kg': weight_kg,
                'hair_color': hair_color,
                'distinctive_marks': distinctive_marks,
            })
            request.session['child_locator_data'] = data

            return redirect(f"{reverse('reportcase')}?{urlencode({'step': 3})}")

        # Step 3: Last Known Location
        elif step == 3:
            last_seen_location = request.POST.get('last_seen_location')
            last_seen_date = request.POST.get('last_seen_date')
            last_known_clothing = request.POST.get('last_known_clothing', '')

            data.update({
                'last_seen_location': last_seen_location,
                'last_seen_date': last_seen_date,
                'last_known_clothing': last_known_clothing,
            })
            request.session['child_locator_data'] = data

            return redirect(f"{reverse('reportcase')}?{urlencode({'step': 4})}")

        # Step 4: Contact Information & Save Data
        elif step == 4:
            guardian_name = request.POST.get('guardian_name')
            contact_number = request.POST.get('contact_number')
            email = request.POST.get('email')

            data.update({
                'guardian_name': guardian_name,
                'contact_number': contact_number,
                'email': email
            })

            # Retrieve stored image path
            image_path = request.session.pop('child_locator_image', None)

            # Save to database
            case = ChildLocator.objects.create(**data)

            if image_path:
                case.image.name = image_path  # Assign stored image path to model
                case.save()

            # Send email notification to all registered users
            send_email_notification(case)

            # Clear session data
            request.session.pop('child_locator_data', None)

            return HttpResponse("<script>alert('Case Submitted. Under Verification'); window.location.href='/home1/';</script>")

    return render(request, 'reportcase.html', {'step': step})

def send_email_notification(case):
    """Send email notification to all registered users about the new missing child case."""
    # Get all registered users
    all_users = models.register.objects.all()
    
    # Prepare email content
    subject = f"ALERT: Missing Child Report - {case.full_name}"
    message = f"""
A new missing child case has been reported:

Name: {case.full_name}
Age: {calculate_age(case.date_of_birth) if case.date_of_birth else 'Not provided'}
Gender: {case.gender}
Last seen: {case.last_seen_location} on {case.last_seen_date}
Last known clothing: {case.last_known_clothing}

Physical description:
- Height: {case.height_cm} cm
- Weight: {case.weight_kg} kg
- Hair color: {case.hair_color}
- Distinctive marks: {case.distinctive_marks}

If you have any information about this child, please contact:
Guardian: {case.guardian_name}
Phone: {case.contact_number}
Email: {case.email}

This is an automated alert. Please do not reply to this email.
    """
    
    # Get sender email from settings
    from_email = settings.EMAIL_HOST_USER
    
    # Send email to each registered user
    recipient_list = [user.email for user in all_users]
    
    # Send emails in batches to avoid timeout issues
    batch_size = 50
    for i in range(0, len(recipient_list), batch_size):
        batch = recipient_list[i:i+batch_size]
        send_mail(subject, message, from_email, batch, fail_silently=False)

def calculate_age(birth_date_str):
    """Calculate age from birth date string."""
    from datetime import datetime
    try:
        # Assuming date format is YYYY-MM-DD
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return f"{age} years"
    except:
        return "Unknown"


from django.shortcuts import render, redirect
from django.urls import reverse
from .models import ChildLocator

def verification(request):
    ver = ChildLocator.objects.filter(accept=False)
    return render(request, 'verification.html', {'ver': ver})

def accept_case(request, case_id):
    case = ChildLocator.objects.get(id=case_id)
    case.accept = True
    case.save()
    return redirect(reverse('listcase'))

from django.shortcuts import render
from .models import NewCase

# def home1(request):
#     new_cases = NewCase.objects.all()  # Get all missing child cases
#     return render(request, 'home1.html', {'new_cases': new_cases})


from django.shortcuts import render
from .models import Feedback, NewCase

def home1(request):
    new_cases = NewCase.objects.all()  # Existing data
    feedbacks = Feedback.objects.all()  # Fetch all feedback entries
    return render(request, 'home1.html', {
        'new_cases': new_cases,
        'feedbacks': feedbacks
    })

from django.contrib import messages

def feedback(request):
    if 'email' in request.session:
        email = request.session['email']
        user = models.register.objects.get(email=email)
        if request.method=='POST':
            rating = request.POST.get('rating')
            comments = request.POST.get('comments')

            models.Feedback(user=user, rating=rating, comments=comments).save()
            messages.success(request, 'Feedback Submitted Successfull')
            return redirect('home1')
        else:
            return render(request, 'feedback.html')
    else:
        return redirect('login')
    
def view_feedback(request):
    feed=models.Feedback.objects.all()
    return render(request,'view_feedback.html',{'feed':feed})
    
# Comparison

# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import NewCase, ChildLocator
# import cv2
# import numpy as np
# import os
# from django.conf import settings
# import tempfile

# def face_comparison_view(request):
#     if request.method == 'POST' and request.FILES.get('uploaded_image'):
#         uploaded_image = request.FILES['uploaded_image']
        
#         # Save the uploaded image to a temporary file
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
#             for chunk in uploaded_image.chunks():
#                 temp_file.write(chunk)
#             temp_file_path = temp_file.name
            
#         try:
#             # Load face detector
#             face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
#             # Detect faces in the uploaded image
#             uploaded_img = cv2.imread(temp_file_path)
#             if uploaded_img is None:
#                 os.unlink(temp_file_path)
#                 return render(request, 'face_comparison_result.html', {
#                     'error': 'Failed to process the uploaded image.'
#                 })
                
#             gray_uploaded = cv2.cvtColor(uploaded_img, cv2.COLOR_BGR2GRAY)
#             faces = face_detector.detectMultiScale(gray_uploaded, 1.1, 5)
            
#             if len(faces) == 0:
#                 os.unlink(temp_file_path)
#                 return render(request, 'face_comparison_result.html', {
#                     'error': 'No faces detected in the uploaded image.'
#                 })
                
#             # Extract the largest face from the uploaded image
#             largest_face = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)[0]
#             x, y, w, h = largest_face
#             uploaded_face = gray_uploaded[y:y+h, x:x+w]
#             uploaded_face = cv2.resize(uploaded_face, (100, 100))
            
#             # Process NewCase images
#             newcase_matches = []
#             for case in NewCase.objects.filter(photo__isnull=False):
#                 try:
#                     case_img_path = case.photo.path
#                     if not os.path.exists(case_img_path):
#                         continue
                        
#                     case_img = cv2.imread(case_img_path)
#                     gray_case = cv2.cvtColor(case_img, cv2.COLOR_BGR2GRAY)
#                     case_faces = face_detector.detectMultiScale(gray_case, 1.1, 5)
                    
#                     if len(case_faces) > 0:
#                         # Get the largest face
#                         case_face = sorted(case_faces, key=lambda x: x[2] * x[3], reverse=True)[0]
#                         x, y, w, h = case_face
#                         case_face_img = gray_case[y:y+h, x:x+w]
#                         case_face_img = cv2.resize(case_face_img, (100, 100))
                        
#                         # Compare faces using various methods
#                         # Method 1: Template matching
#                         score_template = cv2.matchTemplate(uploaded_face, case_face_img, cv2.TM_CCORR_NORMED)[0][0]
                        
#                         # Method 2: Histogram comparison
#                         hist1 = cv2.calcHist([uploaded_face], [0], None, [256], [0, 256])
#                         hist2 = cv2.calcHist([case_face_img], [0], None, [256], [0, 256])
#                         cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
#                         cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)
#                         score_hist = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
                        
#                         # Method 3: Mean Squared Error (MSE)
#                         err = np.sum((uploaded_face.astype("float") - case_face_img.astype("float")) ** 2)
#                         err /= float(uploaded_face.shape[0] * uploaded_face.shape[1])
#                         # Convert MSE to similarity score (higher is better)
#                         max_mse = 255 ** 2  # Maximum possible MSE
#                         score_mse = 1 - (err / max_mse)
                        
#                         # Combine scores
#                         avg_score = (score_template + score_hist + score_mse) / 3
#                         confidence = avg_score * 100
                        
#                         # Only add if confidence is above threshold
#                         if confidence > 60:  # Adjust threshold as needed
#                             newcase_matches.append({
#                                 'case': case,
#                                 'confidence': round(confidence, 2),
#                                 'model_type': 'NewCase'
#                             })
#                 except Exception as e:
#                     continue
            
#             # Process ChildLocator images
#             childlocator_matches = []
#             for locator in ChildLocator.objects.filter(image__isnull=False):
#                 try:
#                     locator_img_path = locator.image.path
#                     if not os.path.exists(locator_img_path):
#                         continue
                        
#                     locator_img = cv2.imread(locator_img_path)
#                     gray_locator = cv2.cvtColor(locator_img, cv2.COLOR_BGR2GRAY)
#                     locator_faces = face_detector.detectMultiScale(gray_locator, 1.1, 5)
                    
#                     if len(locator_faces) > 0:
#                         # Get the largest face
#                         locator_face = sorted(locator_faces, key=lambda x: x[2] * x[3], reverse=True)[0]
#                         x, y, w, h = locator_face
#                         locator_face_img = gray_locator[y:y+h, x:x+w]
#                         locator_face_img = cv2.resize(locator_face_img, (100, 100))
                        
#                         # Compare faces using the same methods
#                         score_template = cv2.matchTemplate(uploaded_face, locator_face_img, cv2.TM_CCORR_NORMED)[0][0]
                        
#                         hist1 = cv2.calcHist([uploaded_face], [0], None, [256], [0, 256])
#                         hist2 = cv2.calcHist([locator_face_img], [0], None, [256], [0, 256])
#                         cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
#                         cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)
#                         score_hist = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
                        
#                         err = np.sum((uploaded_face.astype("float") - locator_face_img.astype("float")) ** 2)
#                         err /= float(uploaded_face.shape[0] * uploaded_face.shape[1])
#                         max_mse = 255 ** 2
#                         score_mse = 1 - (err / max_mse)
                        
#                         avg_score = (score_template + score_hist + score_mse) / 3
#                         confidence = avg_score * 100
                        
#                         if confidence > 60:
#                             childlocator_matches.append({
#                                 'case': locator,
#                                 'confidence': round(confidence, 2),
#                                 'model_type': 'ChildLocator'
#                             })
#                 except Exception as e:
#                     continue
            
#             # Clean up the temporary file
#             os.unlink(temp_file_path)
            
#             # Combine and sort all matches by confidence
#             all_matches = newcase_matches + childlocator_matches
#             all_matches.sort(key=lambda x: x['confidence'], reverse=True)

#             return render(request, 'face_comparison_result.html', {
#             'matches': all_matches,
#             'total_matches': len(all_matches)
#             })
            
#         except Exception as e:
#             # Clean up and return error
#             os.unlink(temp_file_path)
#             return render(request, 'face_comparison_result.html', {
#                 'error': f'An error occurred during face comparison: {str(e)}'
#             })
    
#     # If GET request, show the upload form
#     return render(request, 'face_comparison_upload.html')

from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
import cv2
import numpy as np
import os
from .models import NewCase, ChildLocator
from django.http import JsonResponse
import urllib.request

from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import os

from .models import NewCase, ChildLocator


# ------------------------------------------------------------------
# DeepFace-based face matching (REPLACES OpenCV logic)
# ------------------------------------------------------------------
def match_faces(image1_path, image2_path):
    """
    Compare two face images using DeepFace (ArcFace model)
    Returns a confidence score between 0 and 1 (higher = better match)
    """
    try:
        from deepface import DeepFace  # lazy import (important)

        result = DeepFace.verify(
            img1_path=image1_path,
            img2_path=image2_path,
            model_name="ArcFace",
            detector_backend="retinaface",
            enforce_detection=False
        )

        # DeepFace gives distance (lower is better)
        distance = result["distance"]

        # Convert distance to confidence-like score
        confidence = max(0, 1 - distance)

        return confidence

    except Exception as e:
        print("DeepFace error:", e)
        return 0


# ------------------------------------------------------------------
# Match detection + email notification
# ------------------------------------------------------------------
def send_match_notification(request, detected_image_path, current_location):
    """
    Compare the uploaded image with all images in NewCase and ChildLocator models
    Send email notification for the highest confidence match
    """
    if not os.path.exists(detected_image_path):
        return JsonResponse({'status': 'error', 'message': 'Detected image not found'})

    new_cases = NewCase.objects.filter(status='active')
    child_locators = ChildLocator.objects.filter(accept=True)

    best_match = {
        'confidence': 0,
        'model_type': None,
        'record_id': None
    }

    # Check matches in NewCase
    for case in new_cases:
        if not case.photo or not case.photo.path:
            continue

        confidence = match_faces(detected_image_path, case.photo.path)
        if confidence > best_match['confidence']:
            best_match = {
                'confidence': confidence,
                'model_type': 'NewCase',
                'record_id': case.id
            }

    # Check matches in ChildLocator
    for locator in child_locators:
        if not locator.image or not locator.image.path:
            continue

        confidence = match_faces(detected_image_path, locator.image.path)
        if confidence > best_match['confidence']:
            best_match = {
                'confidence': confidence,
                'model_type': 'ChildLocator',
                'record_id': locator.id
            }

    # ✅ Correct threshold for DeepFace
    threshold = 0.6

    if best_match['confidence'] < threshold:
        return render(request, 'no_match.html', {
            'confidence': round(best_match['confidence'], 3),
        })

    # Prepare email content
    if best_match['model_type'] == 'NewCase':
        case = NewCase.objects.get(id=best_match['record_id'])
        recipient_email = case.guardian_email
        child_name = case.childname
        guardian_name = case.guardian_name

    else:
        locator = ChildLocator.objects.get(id=best_match['record_id'])
        recipient_email = locator.email
        child_name = locator.full_name
        guardian_name = locator.guardian_name

    subject = f"URGENT: Potential match found for {child_name}"

    message = f"""
Dear {guardian_name},

Our system has detected a potential match for your child, {child_name}.

Current Location:
{current_location}

Google Maps Link:
https://www.google.com/maps?q={current_location.replace(' ', '+')}

Please contact authorities immediately.

This is an automated high-priority alert.

Sincerely,
Child Finder System
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=False,
    )

    context = {
        'confidence': round(best_match['confidence'], 3),
        'child_name': child_name,
        'location': current_location,
        'map_link': f"https://www.google.com/maps?q={current_location.replace(' ', '+')}",
        'email_sent': True,
        'recipient': recipient_email
    }

    return render(request, 'match_result.html', context)


# ------------------------------------------------------------------
# Image upload view (UNCHANGED as requested)
# ------------------------------------------------------------------
def detect_face(request):
    """
    View to handle face detection and matching
    """
    if request.method == 'POST':
        if 'image' in request.FILES:
            uploaded_image = request.FILES['image']
            temp_path = os.path.join(settings.MEDIA_ROOT, 'temp_uploads', uploaded_image.name)

            os.makedirs(os.path.dirname(temp_path), exist_ok=True)

            with open(temp_path, 'wb+') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)

            current_location = request.POST.get('location', 'Unknown location')

            return send_match_notification(request, temp_path, current_location)

    return render(request, 'face_detection.html')





# Recovery
def add_recovery_case(request):
    # Get lists of open cases from both models
    child_locator_cases = ChildLocator.objects.all()
    new_cases = NewCase.objects.all()
    
    if request.method == 'POST':
        case_type = request.POST.get('case_type')
        case_id = request.POST.get('case_id')
        date_disappearance = request.POST.get('date_disappearance')
        description = request.POST.get('description')
        suspected_causes = request.POST.get('suspected_causes')
        who_involved = request.POST.get('who_involved')
        tools_methods = request.POST.get('tools_methods')
        found_location = request.POST.get('found_location')
        who_found = request.POST.get('who_found')
        recovery_wellbeing = request.POST.get('recovery_wellbeing')
        legal_actions = request.POST.get('legal_actions')
        submitted_by = request.POST.get('submitted_by')
        
        try:
            # Create new recovery case
            recovery_case = models.ChildRecoveryCase(
                date_disappearance=date_disappearance,
                description=description,
                suspected_causes=suspected_causes,
                who_involved=who_involved,
                tools_methods=tools_methods,
                found_location=found_location,
                who_found=who_found,
                recovery_wellbeing=recovery_wellbeing,
                legal_actions=legal_actions,
                submitted_by=submitted_by
            )
            
            # Link to appropriate case based on case_type
            if case_type == 'childloc':
                childloc_case = ChildLocator.objects.get(id=case_id)
                recovery_case.childloc = childloc_case
                # Send notification about case closure
                send_recovery_notification(case_type, childloc_case)
            else:  # case_type is 'newcase'
                new_case = NewCase.objects.get(id=case_id)
                recovery_case.case = new_case
                # Send notification about case closure
                send_recovery_notification(case_type, new_case)
            
            recovery_case.save()
            
            return HttpResponse("<script>alert('Recovery Case Submitted Successfully'); window.location.href='/adminhome/';</script>")
        
        except Exception as e:
            return HttpResponse(f"<script>alert('Error: {str(e)}'); window.location.href='/add_recovery_case/';</script>")
    
    context = {
        'child_locator_cases': child_locator_cases,
        'new_cases': new_cases
    }
    
    return render(request, 'add_recovery_case.html', context)


def send_recovery_notification(case_type, case_obj):
    """Send email notification to all registered users about the recovered child case."""
    try:
        # Get all registered users
        all_users = models.register.objects.all()
        
        # Prepare email based on case type
        if case_type == 'childloc':
            subject = f"GOOD NEWS: Child Found - {case_obj.full_name}"
            child_name = case_obj.full_name
            child_age = calculate_age(case_obj.date_of_birth) if case_obj.date_of_birth else "Not provided"
            guardian_name = case_obj.guardian_name
            guardian_contact = case_obj.contact_number
        else:  # case_type is 'newcase'
            subject = f"GOOD NEWS: Child Found - {case_obj.childname}"
            child_name = case_obj.childname
            child_age = calculate_age(case_obj.dob) if case_obj.dob else "Not provided"
            guardian_name = case_obj.guardian_name
            guardian_contact = case_obj.guardian_phone
        
        message = f"""
CHILD FOUND - CASE CLOSED

We are pleased to inform you that {child_name}, age {child_age}, 
who was previously reported missing, has been found.

The family has been notified and the case has been closed.

Thank you to everyone who helped with information or shared 
the missing child alert.

For privacy reasons, additional details about the recovery 
are not being disclosed at this time.

If you have any questions, please contact the child's guardian: 
{guardian_name} at {guardian_contact}.

This is an automated message. Please do not reply to this email.
"""
        
        # Get sender email from settings
        from_email = settings.EMAIL_HOST_USER
        
        # Send email to each registered user in batches
        recipient_list = [user.email for user in all_users]
        
        # Send emails in batches to avoid timeout issues
        batch_size = 50
        for i in range(0, len(recipient_list), batch_size):
            batch = recipient_list[i:i+batch_size]
            send_mail(subject, message, from_email, batch, fail_silently=True)
            
    except Exception as e:
        # Log the error but don't stop the case submission
        print(f"Error sending recovery notification emails: {str(e)}")

def calculate_age(birth_date_str):
    """Calculate age from birth date string."""
    from datetime import datetime
    try:
        # Assuming date format is YYYY-MM-DD
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return f"{age} years"
    except:
        return "Unknown"
    
def view_childrecovery(request):
    rec=models.ChildRecoveryCase.objects.all()
    return render(request,'view_childrecovery.html',{'rec':rec})






import cv2
import os
from deepface import DeepFace
from django.conf import settings

def analyze_video(video_path):
    """
    Extract frames from the video and compare with images inside
    media/child_locator_images.
    """

    child_folder = os.path.join(settings.MEDIA_ROOT, "child_locator_images")
    child_images = [os.path.join(child_folder, img) for img in os.listdir(child_folder)]

    if not child_images:
        return None, None, "No child images found"

    # Open video
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    best_match = None
    best_score = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % 10 != 0:
            continue  # analyze every 10th frame

        try:
            # Save temp frame
            temp_frame_path = os.path.join(settings.MEDIA_ROOT, "temp_frame.jpg")
            cv2.imwrite(temp_frame_path, frame)

            # Compare with each child image
            for child_img in child_images:
                try:
                    result = DeepFace.verify(img1_path=temp_frame_path,
                                             img2_path=child_img,
                                             enforce_detection=False)

                    similarity = 1 - result["distance"]

                    if similarity > best_score:
                        best_score = similarity
                        best_match = child_img

                except Exception:
                    continue

        except Exception:
            continue

    cap.release()

    if best_match:
        return best_match, float(best_score), "Match found"
    else:
        return None, None, "No match found"



from django.shortcuts import render
from django.core.files.storage import default_storage

from .models import VideoScan

def detect_child_from_video(request):
    match_path = None
    confidence = None
    status_msg = None

    if request.method == "POST" and request.FILES.get("video"):
        video_file = request.FILES["video"]

        # Save uploaded video
        video_path = default_storage.save(f"uploaded_videos/{video_file.name}", video_file)
        full_video_path = default_storage.path(video_path)

        # Run DeepFace matching
        match_path, confidence, status_msg = analyze_video(full_video_path)

        # Save to database
        VideoScan.objects.create(
            video=video_path,
            matched_child=match_path,
            confidence=confidence
        )

        # Convert full path to MEDIA URL
        if match_path:
            match_path = match_path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)

    return render(request, "child_locator.html", {
        "match_image": match_path,
        "confidence": confidence,
        "status": status_msg
    })



from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from .models import SocialPost
from .face_matcher import match_with_missing_children

def upload_post(request):
    if request.method == "POST":
        img = request.FILES.get("image")
        caption = request.POST.get("caption", "")
        name = request.POST.get("name", "Anonymous")

        # Save uploaded post
        post = SocialPost.objects.create(
            user_name=name,
            caption=caption,
            image=img
        )

        # Absolute path of uploaded image
        uploaded_image_path = default_storage.path(post.image.name)

        # Run DeepFace comparison
        match_with_missing_children(uploaded_image_path)

        return redirect("view_posts")

    return render(request, "upload_post.html")



def view_posts(request):
    posts = SocialPost.objects.all().order_by("-created_at")
    return render(request, "view_posts.html", {"posts": posts})
