from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Recruiter
from .models import StudentUser
from django.views.decorators.csrf import csrf_exempt
from datetime import date

# Create your views here.

def index(request):
    return render(request, 'index.html')

def footer(request):
    return render(request, 'footer.html')

def admin_login(request):
    error=""
    if request.method=='POST':
        u=request.POST['uname']
        p=request.POST['password']
        user=authenticate(username=u,password=p)
        try:
            if user.is_staff:
               login(request,user)
               error="no"
            else:
                 error="yes"
        except:
            error="yes"
    d={'error':error}
    return render(request, 'admin_login.html',d)

def user_login(request):
    error = ""
    if request.method == "POST":
        uname = request.POST.get("uname")  # Use .get() to prevent KeyError
        password = request.POST.get("password")

        if uname and password:  # Ensure both fields are provided
            user = authenticate(username=uname, password=password)
            if user:
                login(request, user)
                return render(request, "user_login.html", {"error": "no"})
            else:
                return render(request, "user_login.html", {"error": "yes"})

    return render(request, "user_login.html", {"error": error})


def recruiter_login(request):
    error = ""  # Initialize error variable here to avoid UnboundLocalError

    if request.method == 'POST':
        # Retrieve the form data
        username = request.POST.get('uname')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.status == "pending":  # Check if the status is "pending"
                    error = "pending_approval"  # Set error message to inform the user
                elif user1.type == "recruiter":  # Ensure it's a recruiter
                    login(request, user)
                    return redirect('recruiter_home')  # Redirect to recruiter home page or dashboard
                else:
                    error = "not_a_recruiter"
            except Recruiter.DoesNotExist:
                error = "no_recruiter_found"
        else:
            error = "invalid_credentials"

    return render(request, 'recruiter_login.html', {'error': error})


def user_home(request):
    if not request.user.is_authenticated:  # ✅ Fixed authentication check
        return redirect('user_login')
    return render(request, 'user_home.html')


def recruiter_pending(request):
    if not request.user.is_authenticated:  # ✅ Fixed authentication check
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='pending')
    d={'data':data}
    return render(request, 'recruiter_pending.html',d)


def recruiter_accepted(request):
    if not request.user.is_authenticated:  # ✅ Fixed authentication check
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='accept')
    d={'data':data}
    return render(request, 'recruiter_accepted.html',d)

def recruiter_rejected(request):
    if not request.user.is_authenticated:  # ✅ Fixed authentication check
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='reject')
    d={'data':data}
    return render(request, 'recruiter_rejected.html',d)

def add_job(request):
    if not request.user.is_authenticated:  # ✅ Fixed authentication check
        return redirect('recruiter_login')
    error=""
    if request.method=='POST':
        j=request.POST['jobtitle']
        s=request.POST['startdate']
        e=request.POST['enddate']
        sa=request.POST['salary']
        l=request.FILES['logo']
        exp=request.POST['experience']
        lo=request.POST['location']
        skil=request.POST['skills']
        des=request.POST['description']
        user=request.user
        recruiter= Recruiter.objects.get(user=user)
        try:
            Job.objects.create(recruiter=recruiter,startdate=s,enddate=e,salary=s,logo=l, experience=exp, location=lo, skills=skil, description=des, creationdate=date.today())
            error="no"
        except:
            error="yes"
    d={'error': error}        
    return render(request, 'add_job.html',d)

def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:  # ✅ Fixed authentication check
        return redirect('recruiter_login')
    error=""
    job=Job.objects.get(id=pid)
    if request.method=='POST':
        j=request.POST['jobtitle']
        s=request.POST['startdate']
        e=request.POST['enddate']
        sa=request.POST['salary']
        l=request.FILES['logo']
        exp=request.POST['experience']
        lo=request.POST['location']
        skil=request.POST['skills']
        des=request.POST['description']

        job.title=job_list
        job.salary=s
        job.experience=exp
        job.location=l
        job.skills=skil
        job.description=des
        try:
            Job.save()
            error="no"
        except:
            error="yes"

    if s:
            try:
                job.start_date=s
                job.save()
            except:
                pass
    else:
         pass
    if e:
            try:
                job.end_date=e
                job.save()
            except:
                pass
    else:
         pass                  
    d={'error': error, 'job': job }      
    return render(request, 'edit_jobdetail.html',d)

def change_companylogo(request,pid):
    if not request.user.is_authenticated:  # ✅ Fixed authentication check
        return redirect('recruiter_login')
    error=""
    job=Job.objects.get(id=pid)
    if request.method=='POST':
        cl=request.FILES['logo']

        job.description=cl
        try:
            Job.save()
            error="no"
        except:
            error="yes"

    d={'error': error, 'job': job }      
    return render(request, 'change_companylogo.html',d)

def job_list(request):
    if not request.user.is_authenticated:  # ✅ Fixed authentication check
        return redirect('recruiter_login')
    user=request.user
    recruiter= Recruiter.objects.get(user=user)
    job= Job.objects.filter(recruiter=recruiter)
    d={'job':job}
    return render(request, 'job_list.html',d)

def recruiter_all(request):
    if not request.user.is_authenticated:  # ✅ Fixed authentication check
        return redirect('admin_login')
    data=Recruiter.objects.all()
    d={'data':data}
    return render(request, 'recruiter_all.html',d)

def change_status(request, pid):
    if not request.user.is_authenticated:  # ✅ Check if the user is logged in
        return redirect('admin_login')
    error =""
    recruiter = Recruiter.objects.get(id=pid)


    if request.method == "POST":
        s = request.POST.get('status')  # ✅ Use .get() to avoid KeyError
        recruiter.status = s  

        try:
            recruiter.save()  # ✅ Save the updated recruiter
            error = "no"
        except Exception as e:
            print(f"Error updating recruiter status: {e}")  # Debugging log
            error = "yes"

    context = {'recruiter': recruiter, 'error': error}
    return render(request, 'change_status.html', context)

def view_users(request):
    if not request.user.is_authenticated:  # ✅ Fixed authentication check
        return redirect('view_users')
    data=StudentUser.objects.all()
    d={'data':data}
    return render(request, 'view_users.html',d)

def admin_home(request):
    if not request.user.is_authenticated:  # ✅ Fixed authentication check
        return redirect('admin_login')
    return render(request, 'admin_home.html')

def Logout(request):
    logout(request)
    return redirect('index')

def recruiter_home(request):
    if not request.user.is_authenticated:  # ✅ Fixed authentication check
        return redirect('recruiter_login')
    return render(request, 'recruiter_home.html')

def user_signup(request):
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        i=request.FILES['image']
        p=request.POST['password']
        e=request.POST['email']
        con=request.POST['contact']
        gen=request.POST['gender']
        try:
            user=User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
            StudentUser.objects.create(user=user, mobile=con, image=i, gender=gen, type="student")
            error="no"
        except:
            error="yes"
    d={'error': error}        
    return render(request,'user_signup.html',d)


def recruiter_signup(request):
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        i=request.FILES['image']
        p=request.POST['password']
        e=request.POST['email']
        con=request.POST['contact']
        gen=request.POST['gender']
        com=request.POST['company']
        try:
            user=User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
            Recruiter.objects.create(user=user, mobile=con, image=i, gender=gen,company=com, type="recruiter",status="pending")

            error="no"
        except:
            error="yes"
    d={'error': error}        
    return render(request, 'recruiter_signup.html',d)

def delete_recruiter(request,pid):
    if not request.user.is_authenticated:  # ✅ Fixed authentication check
        return redirect('admin_login')
    recruiter =User.objects.get(id=pid)
    recruiter.delete()
    return redirect('recruiter_all')

def delete_user(request, pid):
    if not request.user.is_authenticated:  # ✅ Authentication check
        return redirect('admin_login')

    try:
        student = StudentUser.objects.get(id=pid)  # ✅ Fetch student safely
        student.delete()  # ✅ Delete only if found
    except StudentUser.DoesNotExist:
        return redirect('view_users')  # ✅ Redirect if student does not exist

    return redirect('view_users')  # ✅ Redirect after successful deletion

def change_password(request):
    if not request.user.is_authenticated:  # ✅ Check if the user is logged in
        return redirect('admin_login')

    error = ""  # ✅ Initialize error message

    if request.method == "POST":
        c = request.POST.get('currentpassword')  # ✅ Corrected .get() usage
        n = request.POST.get('newpassword')  

        try:
            u = User.objects.get(id=request.user.id)  # ✅ Fetch current user safely
            if u.check_password(c):  # ✅ Verify old password
                u.set_password(n)  # ✅ Update new password
                u.save()  # ✅ Save the updated password
                error = "no"
            else:
                error = "not"  # ✅ Old password didn't match
        except User.DoesNotExist:
            error = "yes"  # ✅ User not found

    context = {'error': error}
    return render(request, 'change_password.html', context)


def change_passworduser(request):
    if not request.user.is_authenticated:  # ✅ Check if the user is logged in
        return redirect('admin_login')

    error = ""  # ✅ Initialize error message

    if request.method == "POST":
        c = request.POST.get('currentpassword')  # ✅ Corrected .get() usage
        n = request.POST.get('newpassword')  

        try:
            u = User.objects.get(id=request.user.id)  # ✅ Fetch current user safely
            if u.check_password(c):  # ✅ Verify old password
                u.set_password(n)  # ✅ Update new password
                u.save()  # ✅ Save the updated password
                error = "no"
            else:
                error = "not"  # ✅ Old password didn't match
        except User.DoesNotExist:
            error = "yes"  # ✅ User not found

    context = {'error': error}
    return render(request, 'change_passworduser.html', context)


def change_passwordrecruiter(request):
    if not request.user.is_authenticated:  # ✅ Check if the user is logged in
        return redirect('recruiter_login')

    error = ""  # ✅ Initialize error message

    if request.method == "POST":
        c = request.POST.get('currentpassword')  # ✅ Corrected .get() usage
        n = request.POST.get('newpassword')  

        try:
            u = User.objects.get(id=request.user.id)  # ✅ Fetch current user safely
            if u.check_password(c):  # ✅ Verify old password
                u.set_password(n)  # ✅ Update new password
                u.save()  # ✅ Save the updated password
                error = "no"
            else:
                error = "not"  # ✅ Old password didn't match
        except User.DoesNotExist:
            error = "yes"  # ✅ User not found

    context = {'error': error}
    return render(request, 'change_passwordrecruiter.html', context)

def job_detail(request,pid):
    job=Job.objects.get(id=pid)
    d={'job':job}
    return render(request, 'job_detail.html',d)

def latest_jobs(request):
    job=Job.objects.all()
    d={'job':job}
    return render(request, 'latest_jobs.html',d)

def user_latestjobs(request):
    job=Job.objects.all()
    user= request.user
    student = StudentUser.objects.get(user=user)
    data = Apply.objects.filter(student= student)
    li=[]
    for i in data:
        li.append(i.job.id)
    d={'job':job,'li': li}
    return render(request, 'user_latestjobs.html',d)
# Check if the password and username are provided
        #if username and password:
           # user = authenticate(request, username=username, password=password)
            #if user is not None:
                # Assuming 'RecruiterUser' model is related to User, you can log the recruiter in
             #   login(request, user)
              #  messages.success(request, "Login successful!")
               # return redirect('recruiter_dashboard')  # Redirect to a recruiter dashboard or home page
            #else:
             #   messages.error(request, "Invalid username or password.")
        #else:
         #   messages.error(request, "Both username and password are required.")
