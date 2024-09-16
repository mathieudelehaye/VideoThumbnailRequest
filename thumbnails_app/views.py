from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import ThumbnailRequest
from paypalrestsdk import Payment
from thumbnails_app.forms import ThumbnailRequestForm
from thumbnails_app.models import ThumbnailRequest

def submit_thumbnail_request(request):
    if request.method == 'POST':
        form = ThumbnailRequestForm(request.POST, request.FILES)
        if form.is_valid():
            thumbnail_request = form.save(commit=False)
            
            # Check if the user is authenticated
            if request.user.is_authenticated:
                thumbnail_request.user = request.user  # Assign the logged-in user
            else:
                # If the user is not authenticated, redirect to login
                return redirect(f'/accounts/login/?next={request.path}')
            
            thumbnail_request.save()
            
            # Redirect to payment or success page
            return redirect('create_payment')
    else:
        form = ThumbnailRequestForm()

    return render(request, 'submit_thumbnail.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect('/')  # Redirect to the home page
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

@login_required  # Ensure only logged-in users can access the account page
def account_page(request):
    # Filter thumbnail requests to only show the ones that belong to the logged-in user
    thumbnails = ThumbnailRequest.objects.filter(user=request.user)
    return render(request, 'account_page.html', {'thumbnails': thumbnails})

@login_required
def create_payment(request):
    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": "10.00",
                "currency": "USD"
            },
            "description": "Video Thumbnail Payment"
        }],
        "redirect_urls": {
            "return_url": "http://localhost:8000/payment/execute/",
            "cancel_url": "http://localhost:8000/payment/cancel/"
        }
    })

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                # Redirect the user to PayPal for payment approval
                return redirect(link.href)
    else:
        print(payment.error)
        return render(request, 'payment_failed.html')

@login_required
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'payment_success.html')
    else:
        return render(request, 'payment_failed.html')

@login_required
def account_page(request):
    user_thumbnails = ThumbnailRequest.objects.filter(user=request.user)
    return render(request, 'account_page.html', {'thumbnails': user_thumbnails})
