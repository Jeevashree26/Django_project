from django.shortcuts import redirect, render
from django.http import  JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from IT_services import settings
from .models import OTP, Service, Subscription
from django.core.mail import send_mail
import random
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .form import ServiceForm
from django.core.exceptions import MultipleObjectsReturned
client = razorpay.Client(auth=("rzp_test_e664V0FP0zQy7N", "QdnuRxUHrPGeiJc9lDTXYPO7"))


# Create your views here.
def home(request):
    services = Service.objects.filter(active=True)
    for service in services:
        service.tax_amount = service.price * service.tax / 100
        service.total_price = service.price + service.tax_amount
    return render(request, "Service/index.html", {"services": services})

def register(request):

    if request.method == "POST":
        username = request.POST['Username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist !")
            return redirect('home')
        
        # if User.objects.filter(email=email):
        #     messages.error(request, "Username already registered !")
        #     return redirect('home')
        
        if len(username)>10:
            messages.error(request, "Username must be under 10 characters")
        
        if password != cpassword:
            messages.error(request, "Passwords didn't match!!")
        
        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        # messages.success(request,"Your account has been successfully Registered, one step ahead to login your account \n please verify you email id ")

        # otp
        otp_code = ''.join(random.choices('0123456789', k=6))
        OTP.objects.create(user=myuser, otp_code=otp_code)

         # Store OTP and email in session
        request.session['email'] = email
        request.session['otp_code'] = otp_code

        #email

        subject = "Welcome to IT_Services - Verify Your Email"
        message = "Hello  " + username + "!!\n"+"Your OTP code is: " + otp_code +"\n Please enter this code to verify your email and activate your account.\n\nThank you for registering with us!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        messages.success(request, "Account created! Please check your email to verify your account.")
        return redirect('verify_otp')  
    
    return render(request,"Service/register.html")

def verify_otp(request):
    if request.method == "POST":
        otp_input = request.POST['otp']
        email = request.session.get('email')
        otp_code = request.session.get('otp_code')

        if email and otp_code:
            if otp_code == otp_input:
                try:
                    users = User.objects.filter(email=email)
                    if users.count() == 1:
                        user = users.first()
                        user.is_active = True
                        user.save()

                        # Clean up session data
                        del request.session['email']
                        del request.session['otp_code']

                        messages.success(request, "Your email has been verified successfully!")
                        return redirect('log_in')
                    else:
                        messages.error(request, "Multiple users found with this email. Contact support.")
                except MultipleObjectsReturned:
                    messages.error(request, "Multiple users found with this email. Contact support.")
            else:
                messages.error(request, "Invalid OTP.")
        else:
            messages.error(request, "OTP verification session expired.")

        return redirect('verify_otp')

    return render(request, "Service/verify_otp.html")

def log_in(request):

    if request.method == "POST":
        username = request.POST['Username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "Service/index.html", {'fname': username})
        else:
            messages.error(request, "Bad credentials")
            return redirect('home')
    return render(request,"Service/log_in.html")

def log_out(request):
    logout(request)
    messages.success(request, "Logged out successfully !")
    return redirect("home")



def create_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service created successfully!")
            return redirect('list_service')
        else:
            messages.error(request, "Please fill in all the required fields.")
    else:
        form = ServiceForm()
    
    return render(request, "Service/create_service.html", {'form': form})


def list_service(request):
    services = Service.objects.all()
    return render(request, "Service/list_service.html", {'services': services})


def update_service(request, pk):
    service = get_object_or_404(Service, pk=pk)

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully!")
            return redirect('list_service')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ServiceForm(instance=service)
    
    return render(request, "Service/update_service.html", {'form': form})


def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == "POST":
        service.delete()
        messages.success(request, "Service deleted successfully!")
        return redirect('list_service')
    
    return render(request, "Service/delete_service.html", {'service': service})



@login_required
def subscribe(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    total_price = service.price + (service.price * service.tax / 100)

    if request.method == "POST":
        address = request.POST.get('address')
        if not address:
            messages.error(request, "Address is required.")
            return render(request, 'Service/subscribe.html', {'service': service})

        # Save subscription details (implement the Subscription model logic as per your need)
        subscription = Subscription(
            user=request.user,
            service=service,
            address=address,
            amount=service.price + (service.price * service.tax / 100),
            payment_status='Pending'  # or any status you'd like to set initially
        )
        subscription.save()
        # Redirect to Razorpay payment
        return redirect('buy_service', service_id=service.id, subscription_id=subscription.id)

    return render(request, 'Service/subscribe.html', {'service': service, 'total_price': total_price})


def buy_service(request, service_id, subscription_id):
    service = get_object_or_404(Service, id=service_id)
    amount = int((service.price + (service.price * service.tax / 100)) * 100)  # Amount in paise
    currency = 'INR'

    # Create Razorpay order
    razorpay_order = client.order.create({
        'amount': amount,
        'currency': currency,
        'payment_capture': '1'  # Auto-capture payment
    })

    context = {
        'service': service,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': "rzp_test_e664V0FP0zQy7N",
        'amount': amount,
        'currency': currency,
        'subscription_id': subscription_id,
    }

    return render(request, 'Service/buy_service.html', context)


@csrf_exempt
def razorpay_callback(request):
    if request.method == 'POST':
        data = request.POST
        payment_id = data.get('razorpay_payment_id')
        order_id = data.get('razorpay_order_id')
        signature = data.get('razorpay_signature')
        subscription_id = data.get('subscription_id')
        
        # if not subscription_id:
        #     return JsonResponse({'status': 'error', 'message': 'Subscription ID is missing'}, status=400)
        # Validate the signature
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })
            
            # Fetch the payment details
            payment = client.payment.fetch(payment_id)
            
            if payment['status'] == 'captured':
                # Update subscription status
                subscription = get_object_or_404(Subscription, id=subscription_id)
                subscription.payment_status = 'Paid'
                subscription.transaction_id = payment_id
                subscription.save()
                
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failed'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)