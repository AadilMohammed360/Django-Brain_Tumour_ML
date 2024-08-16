from django.shortcuts import render, redirect
from .models import * 
import os



from django.shortcuts import render, redirect
from django.http import HttpResponse

from PIL import Image
from django.conf import settings
from pathlib import Path
from PIL import Image




def add_patient_data(request):
    if (request.method=="POST"):
        name = request.POST['name']
        age = request.POST['age']
        print("Age:     " + age)
        fmri_photo = request.FILES['fmri_photo']
        # calculate age from date     
        age=calculate_age(age)
        cur_datetime = datetime.now()
        data=PatientData(name=name,age=age,fmri_photo=fmri_photo,datetime=cur_datetime)
        data.save()   
    return redirect('staff_welcome')


def manageprivacy(request):
    if (request.method=="POST"):
        sid = request.session['log_id']
        username = request.POST['username']
        password = request.POST['password']
        login=Login.objects.get(id=sid)

        if (login.role == "staff"):
            login.username = username
            login.password = password
            login.save()
            staff = Staff.objects.get(log_id=sid)
            staff.name = username
            staff.save()
            return redirect('staff_welcome')   
        elif (login.role == "doctor"):
            login.username = username
            login.password = password
            login.save()
            staff = Doctor.objects.get(log_id=sid)
            staff.name = username
            staff.save()   
            return redirect('doctor_welcome')   
        else:
            login.username = username
            login.password = password
            login.save()  
            return redirect('admin_welcome')   
    return redirect('index')


def privacy(request):
    return render(request,'privacy.html',)




from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify
from django.conf import settings
import os

def rename_uploaded_file(file_name, new_name, file_extension):

    # Construct the new file name with the ID and extension
    new_file_name = f"{slugify(new_name)}{file_extension}"

    # Create a file system storage instance for handling file operations
    fs = FileSystemStorage()

    # Get the full path to the uploaded file
    uploaded_file_path = fs.path(file_name)

    # Create the full path to the new file
    new_file_path = os.path.join(settings.MEDIA_ROOT, 'fmri_photos', new_file_name)

    # Rename the file using the file system storage
    if fs.exists(uploaded_file_path):
        os.rename(uploaded_file_path, new_file_path)

    return new_file_name























def up_patient_data(request):
    if request.method == "POST":
        dataid = request.POST['id']
        fmri_photo = request.FILES['fmri_photo']
        cur_datetime = datetime.now()
        data = PatientData.objects.get(id=dataid)

        # Get the original filename of the uploaded file
        original_file_name = fmri_photo.name

        # Split the filename and extension
        file_name, file_extension = os.path.splitext(original_file_name)
        
        # Save the uploaded file to disk using Django's file system storage
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        saved_file_name = fs.save(fmri_photo.name, fmri_photo)

        # Rename the saved file with the ID appended to the filename
        new_file_name = rename_uploaded_file(saved_file_name, f"{file_name}__({dataid})", file_extension)

        # Update the data object with the new file path
        data.fmri_photo = f"fmri_photos/{new_file_name}"
        data.datetime = cur_datetime
        data.save()

    return redirect('staff_welcome')





















# <--============END OF add patient data=======================-->


# date to age conversino 
from datetime import datetime
from django.http import JsonResponse

def calculate_age(age):

    input_date_str = age # Assuming 'input_date' is the name of the input field
    print("Input: " + input_date_str)
    if input_date_str:
        try:
            input_date = datetime.strptime(input_date_str, '%Y-%m-%d')  # Convert input string to datetime object
            today = datetime.now()  # Get today's date
            age = today.year - input_date.year - ((today.month, today.day) < (input_date.month, input_date.day))
            
            age = age + 1
            print("Age:  " + str(age))
            return age
        except ValueError:
            print("Exception")
    else:
        print("else")




# basic render
def index(request):
    return render(request, 'index.html')

def login_page(request):
    return render(request, 'login.html')

def doctor_welcome(request):
    return render(request, 'doctor_welcome.html')

def admin_welcome(request):
    return render(request, 'admin/welcome.html')

def staff_welcome(request):
    return render(request, 'staff_welcome.html')

def register_patient(request):
    if (request.method=="GET"):
        report = request.GET['report']
        print(report)
        return render(request, 'register_patient.html',{'report':report,})

def view_patient_data(request):
    patientdata = PatientData.objects.all().order_by('-datetime')
    return render(request, 'view_patient_data.html',{'patientdata':patientdata,})

# login 
#account login
def accountlogin(request):
    if(request.method=="POST"):
        username = request.POST['username']
        password = request.POST['password']
        try:
            # Try to retrieve the specific record
            logindata = Login.objects.get(username=username,password=password)
            # Use except on default exception where the object u tried to retrieve do not exist
        except Login.DoesNotExist:
            # Handle the case where the specific record is not found
            logindata = None   
               
        if(logindata!=None):
            request.session['log_id']=logindata.id
            # print(request.session['log_id'])
            if (logindata.role == "staff"):
                # applicantprofile = Applicant.objects.get(username = username, log_id=logindata.id,)
                staffprofile = Staff.objects.get(log_id=logindata.id)
                staffname = staffprofile.name
                # return redirect('staff_welcome')
                # return redirect('apctabout')
                return render(request,'staff_welcome.html',{'staffname':staffname,})
            elif (logindata.role == "doctor"):
                # staffprofile = Staff.objects.get(username = username, log_id=logindata.id,)
                doctorprofile = Doctor.objects.get(log_id=logindata.id)
                doctorname = doctorprofile.name

                # return redirect('doctor_welcome')
                return render(request,'doctor_welcome.html',{'doctorname':doctorname,})
            else :
                return render(request,'admin/welcome.html')            
                
    return render(request,'login.html',)



























# Define your view function
def view_prediction(request):

    if request.method == "GET":
        import os
        file_path = request.GET.get('photo_path')
 
        image_name = os.path.basename(file_path)
        print("image name is" + image_name)

        image_path = './media/fmri_photos/' + image_name

        model_path = 'brain_model_11.keras'


        result = s_pred(image_path, model_path)


        # return HttpResponse(f'passed Machine learning {result}')
        print(result)

        photo_media_path = file_path


        # return HttpResponse(f'Prediction done on image path: {image_path} and result returned as {result} ')
        return render(request, 'pred_result.html', {'result':result, 'photo_media_path':photo_media_path})


import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np



def s_pred(image_path, model_path):
    model = tf.keras.models.load_model(model_path)

    img = image.load_img(image_path, target_size=(256, 256))

    img_array = image.img_to_array(img)

    img_array = np.expand_dims(img_array, axis=0)

    img_array /= 255.

    prediction = model.predict(img_array)

    if prediction[0] > 0.5:
        print("The model predicts this is a Schizophrenia image.")
        return 'Positive'
    else:
        print("The model predicts this is a non-Schizophrenia image.")
        return 'Negative'




# <--==============================Trial and Errors=====================================-->
    # model = CNN_Schizophrenia()
    # prediction = dPred.predict(image_path)
    # print("The patient is Schizophrenia",prediction)

#     # Get the path to the machine learning Python file within the media folder
#     media_dir = settings.MEDIA_ROOT
#     ml_file_path = os.path.join(media_dir, 'ML.py')

#     # Import the MachineLearningClass from the ml_file.py
#     from media.ML import CNN_Schizophrenia, predict, hello
#     ML_instance = CNN_Schizophrenia()
#     hello()

#     # image_path = "fmri_photos/Schizophrenia_22.tif"
#     # prediction = predict(image_path)
#     # print(prediction)


    # return HttpResponse("Python file executed successfully." + image_path)
    

# <------------------------------------ADMIN STAFF MANAGEMENT------------------------------------->

def managestaff(request):
    if request.method == "GET":
        roletype = request.GET['roletype']
        print(roletype)
        staffdata = Staff.objects.all()
        doctordata = Doctor.objects.all()
        return render(request, 'managestaff.html', {'staffdata':staffdata,'roletype':roletype,'doctordata':doctordata})
# account creation and registering users

def registerusers(request):
    if request.method == "POST":
        name = request.POST['name']
        age = request.POST['age']
        username = name
        role = request.POST['role']  # New field for role
        password = role + '123'
        
        # Assuming 'fmri_photo' is not included in this form
        # If 'fmri_photo' is included, make sure to handle it appropriately
        
        # Create a new user or patient record
        logindata = Login(username=username,password=password,role=role)
        logindata.save()

        if(role=="staff"):
            staffdata = Staff(name=name,age=age,log_id=logindata)
            staffdata.save()
            staffdata = Staff.objects.all()
            return render(request, 'managestaff.html', {'staffdata':staffdata,'roletype':role,})

        if(role=="doctor"):
            doctordata = Doctor(name=name,age=age,log_id=logindata)
            doctordata.save()
            doctordata = Doctor.objects.all()
            return render(request, 'managestaff.html', {'doctordata':doctordata,'roletype':role,})



def updatevacancy(request):
    if(request.method=='POST'):
        record_id  = request.POST['recordid']

        newname=request.POST['newname']
        newage=request.POST['newage']
        role=request.POST['role']
        print(record_id)

        if (role == "staff"):

            record = Staff.objects.get(log_id_id=record_id)
            record.name = newname
            record.age = newage
            record.save()        
            logindata = Login.objects.get(id=record_id)
            logindata.username = newname
            logindata.save()

        if (role == "doctor"):

            record = Doctor.objects.get(log_id_id=record_id)
            record.name = newname
            record.age = newage
            record.save()        
            logindata = Login.objects.get(id=record_id)
            logindata.username = newname
            logindata.save()
        staffdata = Staff.objects.all()    
        doctordata = Doctor.objects.all()    
        return render(request, 'managestaff.html', {'staffdata':staffdata,'doctordata':doctordata,'roletype':role,})
    
def removevacancy(request):
    if request.method == "GET":
        role = request.GET['role']
        rowid = request.GET['delid']
        if role =="staff":
            deletedata = Staff.objects.get(log_id_id=rowid)
            logid=deletedata.log_id_id
            deletedata.delete()
            logindata = Login.objects.get(id=logid).delete()
        if role == "doctor":
            deletedata = Doctor.objects.get(log_id_id=rowid)
            logid=deletedata.log_id_id
            deletedata.delete()
            logindata = Login.objects.get(id=logid).delete()
        staffdata = Staff.objects.all()    
        doctordata = Doctor.objects.all()    
        return render(request, 'managestaff.html', {'staffdata':staffdata,'doctordata':doctordata,'roletype':role,})


# <------------------------------------ADMIN STAFF MANAGEMENT------------------------------------->