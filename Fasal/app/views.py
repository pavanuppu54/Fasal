from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from project import settings
from .tokens import generate_token

def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try another username.")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('home')

        if len(username) > 20:
            messages.error(request, "Username must be 20 characters or fewer!")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        # Send confirmation email
        current_site = get_current_site(request)
        email_subject = "ᗰOᐯIEᔕᑎOᗯ @ Confirm your Email"
        email_message = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.send()

        messages.success(request, "Your account has been created! Please check your email to confirm your email address.")
        return redirect('signin')

    return render(request, "authentication/signup.html")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your account has been activated!")
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successfully!")
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials!")

    return render(request, "authentication/signin.html")

from django.shortcuts import redirect

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('/')  # Redirect to the home page directly

from django.core.mail import send_mail

def feedback(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        rating = request.POST.get('rating')

        # Sending feedback via email
        email_subject = f"New Feedback from {name}"
        email_message = f"Name: {name}\nEmail: {email}\nRating: {rating}\n\nMessage:\n{message}"

        send_mail(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_FEEDBACK_RECIPIENT],  # Add this to your settings.py
        )

        messages.success(request, "Thank you for your feedback!")
        return redirect('home')
    return render(request, 'authentication/index.html')
