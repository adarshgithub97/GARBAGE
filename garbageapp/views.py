from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Garbage,Contact,Plant,Booking,PasswordResetToken
from django.views.decorators.csrf import csrf_exempt
import razorpay
# Create your views here.

def index(request):
    return render(request,'index.html')


def about(request):
    return render(request,"about.html")


def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        message=request.POST['message']

        if len(phone) != 10:
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect('garbageapp:contact')
        if Contact.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('garbageapp:contact') 
        
        cont=Contact(name=name,phone=phone,email=email,message=message)
        cont.save()
        messages.success(request, 'Message sent successfully.')
    return render(request,"contact.html")


def types(request):
    return render(request,"waste-type.html")


def booking(request):
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        place = request.POST.get('place')
        waste_type = request.POST.get('waste_type')
        weight = request.POST.get('weight')
        date = request.POST.get('date')
        time = request.POST.get('time')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Enter valid email address")
            return redirect('garbageapp:booking') 

        if len(fname) == 0 or len(lname) == 0 or len(email) == 0 or len(place) == 0:
            messages.error(request, "Please fill all required fields.")
            return redirect('garbageapp:booking') 
            
        try:
            weight = int(weight)  
        except ValueError:
            messages.error(request, "Weight must be a number.")
            return redirect('garbageapp:booking') 
        
        booking = Booking(first_name=fname,last_name=lname,email=email,address=address,place=place,waste_type=waste_type,weight=weight,date=date,time=time)
        booking.save()
        request.session['waste_type'] = waste_type
        request.session['weight'] = weight
        request.session['booking_id'] = booking.id
        return redirect('garbageapp:map')
    return render(request,"waste-booking.html")


def is_strong_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters."
    if not re.search(r'[A-Za-z]', password):
        return "Password must contain at least<br>one albhabet."
    if not re.search(r'[0-9]', password):
        return "Password must contain at least<br> one digit."
    if not re.search(r'[@$!%*?&#]', password):
        return "Password must contain at least<br> one special character."
    return None


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password != cpassword:
            messages.error(request, "Passwords do not match.")
            return redirect('garbageapp:register')
        if Garbage.objects.filter(email=email).exists():
            messages.error(request, "Email already exits.")
            return redirect('garbageapp:register')
        if Garbage.objects.filter(username=username).exists():
            messages.error(request, "Username already exits.")
            return redirect('garbageapp:register')
        
        password_error = is_strong_password(password)
        if password_error:
            messages.error(request, password_error)
            return redirect('garbageapp:register')

        user = Garbage(username=username, email=email, password=password, cpassword=cpassword)
        user.save()
        return redirect('garbageapp:login') 
    return render(request,'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Please enter both email and password.')
            return render(request, 'login.html')
        
        try:
            user = Garbage.objects.get(email=email)
        except Garbage.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return render(request, 'login.html')

        if user.password == password:
            user_data = {
                'username': user.username,
                'email': user.email
            }
            request.session['user'] = user_data
            return redirect('garbageapp:types')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('garbageapp:login')
    return render(request, 'login.html')


def logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('garbageapp:login')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Garbage.objects.get(email=email)
            # Create a password reset token
            token = PasswordResetToken.objects.create(user=user)
            # Redirect to the reset password page
            return redirect('garbageapp:reset_password', token=token.token)
        except Garbage.DoesNotExist:
            messages.error(request, 'Email does not exist.')
            return redirect('garbageapp:forgot_password')
    return render(request, 'forgot_password.html')


def reset_password(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token, is_active=True)
        if not reset_token.is_token_valid():
            messages.error(request, 'Token is invalid or has expired.')
            return redirect('garbageapp:forgot_password')
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid token.')
        return redirect('garbageapp:forgot_password')

    if request.method == 'POST':
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password != cpassword:
            messages.error(request, "Passwords do not match.")
            return redirect('garbageapp:reset_password', token=token)
        
         # Check password strength
        strength_error = is_strong_password(password)
        if strength_error:
            messages.error(request, strength_error)
            return redirect('garbageapp:reset_password', token=token)

        # Update the user's password
        user = reset_token.user
        user.password = password
        user.cpassword = cpassword
        user.save()
        # Invalidate the token.Once the password has been reset, the token is marked as inactive so that it cannot be reused.
        reset_token.is_active = False
        reset_token.save()

        messages.success(request, "Password has been reset successfully.")
        return redirect('garbageapp:login')
    return render(request, 'reset_password.html')


def map(request):
    if not request.session.get('booking_id'):
        return redirect('garbageapp:booking')
    return render(request,"map.html")
  


def plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    # Retrieve the booking from the session and update it
    booking_id = request.session.get('booking_id')
    if booking_id:
        booking = Booking.objects.get(id=booking_id)
        booking.selected_plant = plant
        booking.save()
        # Remove booking from session since it is completed
        del request.session['booking_id']
    return render(request, "plantation.html", {'detail': plant})

    
def sample(request):
    return render(request,'plantation')

def payment(request):
    waste_type = request.session.get('waste_type')
    weight = request.session.get('weight')
    amount = weight * 100 + 100  

    # Create Razorpay order with dynamic amount
    client = razorpay.Client(auth=("rzp_test_JAeLcxoJpwFjEq", "PvjOeaEQA5b2gH4XHxEGEhMB"))

    payment = client.order.create({
        'amount': amount * 100,  # Convert to paise
        'currency': 'INR',
        'payment_capture': '1'
    })

    context = {
        'waste_type': waste_type,
        'weight': weight,
        'amount': amount,
        'payment': payment,
    }
    return render(request, 'payment.html', context)


@csrf_exempt
def success(request):
    return render(request, 'success.html')


def home1(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 500  # This will be overridden in payment view

        client = razorpay.Client(
            auth=("rzp_test_JAeLcxoJpwFjEq", "PvjOeaEQA5b2gH4XHxEGEhMB"))

        payment = client.order.create({'amount': amount * 100, 'currency': 'INR',
                                       'payment_capture': '1'})
    return render(request, 'success.html')  


