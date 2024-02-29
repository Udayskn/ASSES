from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponse

# Create your views here.
def login_func(request):
    if request.method == 'POST':
        username,password = request.POST['username'],request.POST['password']

        ## checking if user exists or not
        u = authenticate(request,username=username,password=password)

        if u is not None:
            print('A login occured')
            logout(request)
            login(request,u)
            '''CHANGE HERE IF YOU WANT TO REDIRECT TO HOME'''
            return HttpResponse('Successfully logged in!')
        else:
            print("Failed Login")
            redirect('AUTHENTICATION:login') # 'APPNAME:URLNAME'

    return render(request,'AUTHENTICATION/login.html')

def signin_func(request):
    if request.method == 'POST': # it means we are getting req to add user
        # when addding some attributes to user,modify below:
        username,password1,password2,email = request.POST['username'],request.POST['password1'],request.POST['password2'],request.POST['email']
        
        if password1==password2:
            try:
                u = User.objects.create_user(username,email,password1)
                u.save()
                print('User added')
                return redirect('AUTHENTICATION:login')
            except:
                #modify this for better representing error
                return HttpResponse("Username or email already exits!")
        else:
            return redirect("AUTHENTICATION:signin")

    return render(request,'AUTHENTICATION/signin.html')
        
