from datetime import datetime
from django import conf
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.base import TemplateView
from .models import Profile, GenerateCodes
from posts.models import Post
from django.contrib.auth.models import User
from django.http import JsonResponse
from doctor.models import Notifications
from django.views.generic import ListView, DetailView
from .forms import ImageUploadForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


# Create your views here.
# def SendMailer(user, )
# print(datetime.now())


def check_code_validity(code):
    try:
        profile = GenerateCodes.objects.get(token=code)
        # check expiry
        if profile.has_expired:
            return "expired"
        else:
            return "valid"
    except GenerateCodes.DoesNotExist:
        return "error"


def Send_code_by_mail(user, email, template="reset_password.html", reason=""):
    """
        Sends a code to users via email.

        Args:
            user(object, required): Current user in session.
            reason(String, optional): Use of the code! (because I like it that way!)
        Returns:
            error: If user has no email
            success: If email was sent successfully
    """
    # user's full name(includes the username too!)
    name = user.first_name + " "+user.last_name+" "+user.username

    # check if the user email already exists
    if user.email:
        email = user.email
    else:
        return JsonResponse({"error": "User with the given email does not exist"}, status=400)

    try:
        # check if the user already has a code already
        now = timezone.now()  # current datetime
        profile = GenerateCodes.objects.filter(
            user=user).order_by("-generated_on")[0]
        check_1 = check_code_validity(profile.token)
        if check_1 == "valid":
            # was found, so resend it.
            pass
        elif check_1 == "expired":
            # delete the expired and send a new one
            profile.delete()
            profile = GenerateCodes.objects.create(user=user, reason=reason)
        elif check_1 == "error":
            # was not found, continue to create a new one
            profile = GenerateCodes.objects.create(user=user, reason=reason)
    except GenerateCodes.DoesNotExist:
        # create one
        profile = GenerateCodes.objects.create(user=user, reason=reason)

    subject = profile.reason
    # for html visible browsers
    html_message = render_to_string("mail_templates/"+template, {
        'name': name,
        "instance": profile,
        'code': profile.token,
    })
    # for crippled browser
    message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to_email = email

    sender = send_mail(subject=subject, message=message, from_email=from_email,
                       recipient_list=[to_email], html_message=html_message)
    if sender:
        return True
    else:
        return False


def request_code(request):
    if request.is_ajax():
        # if an email was sent via POST request
        email = request.POST.get("email")
        if email:
            email = request.POST.get("email")
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({"message": "User with provided email does not exist", "status": False})
        # if it was not sent but the user is logged in!
        try:

            sender = Send_code_by_mail(
                user, email, reason="YieldUp Reset Password")
            return JsonResponse({"message": "Code sent to your email", "status": True})
        except Exception as e:
            print(e)
            return JsonResponse({"message": "Something went wrong, please try again", "status": False})
    return render(request, "auths/forgot_password.html")


class EnterCodeView(TemplateView):
    template_name = "auths/enter_token.html"


def check_expiriration(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"message": "Code is required", "status": False})
    checker = check_code_validity(code)
    if checker == "valid":
        return JsonResponse({"message": "Code is valid", "status": True})
    elif checker == "expired":
        return JsonResponse({"message": "Code is expired", "status": False})
    elif checker == "error":
        return JsonResponse({"message": "Code does not exist", "status": False})
    return JsonResponse({"message": "Something went wrong, please try again", "status": False})


def ResetPassword(request, code):
    if request.is_ajax():
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]
        print(new_password)
        print(confirm_password)
        if new_password != confirm_password:
            return JsonResponse({"error": "Passwords are not matching"})
        elif len(confirm_password) < 8:
            return JsonResponse({"error": "Password is too week"})
        else:
            checker = check_code_validity(code)
            if checker == "valid":
                profile = GenerateCodes.objects.get(token=code)
                profile.user.set_password(new_password)
                profile.user.save()
                profile.delete()
                return JsonResponse({"success": "Password changed successfully"})
            elif checker == "expired":
                return JsonResponse({"error": "Code is expired"})
            elif checker == "error":
                return JsonResponse({"error": "Code does not exist"})
    return render(request, "auths/recover_password.html", {"code": code})


class UserListView(ListView):
    model = Profile
    context_object_name = 'users'
    template_name = "profiles/all_users.html"

    def get_queryset(self):
        return Profile.objects.all()


@login_required(login_url='/login/')
def UpdateProfileImage(request):
    if request.method == 'POST':
        myImage = request.FILES['pimage']
        myprofile = get_object_or_404(Profile, user=request.user)
        myprofile.profile_pik = myImage
        myprofile.save()

    return redirect('profile:profile_for')


# get a single user
@login_required(login_url='/login/')
def SingleUser(request, pk):
    context = {}
    # form = ImageUploadForm()
    context['profile'] = Profile.objects.get(pk=pk)
    context['posts'] = Post.objects.filter(posted_by=request.user)
    context['received_notifications'] = Notifications.objects.filter(
        to__user=request.user)
    context['sent_notifications'] = Notifications.objects.filter(
        fro__user=request.user)

    if request.method == 'GET':
        if request.is_ajax():
            if request.GET.get('flag'):
                user = request.user
                user.delete()
                return JsonResponse({"message": 'User deleted successfully', "code": True})

    if request.method == 'POST':
        if request.is_ajax():

            if request.POST.get('updating_password'):
                if request.POST.get('password1') != '' and request.POST.get('password2') != '':
                    current_password = request.user.password
                    matchcheck = check_password(
                        request.POST.get('password1'), current_password)
                    if matchcheck:
                        user = User.objects.get(pk=request.user.id)
                        user.set_password(request.POST.get('password2'))
                        user.save()
                        return JsonResponse({"message": 'Password updated successfully, logging you out!', "code": True})
                    else:
                        return JsonResponse({"message": 'No account is associated with the given password!', "code": False})
                else:
                    return JsonResponse({"message": 'Some fields are still empty', "code": False})

            if request.POST.get('update_advanced'):
                if request.POST.get('email') != '' and request.POST.get('last_name') != '' and request.POST.get('username') != '' and request.POST.get('first_name') != '':
                    user = User.objects.get(pk=request.user.id)
                    try:
                        new_user = User.objects.get(
                            email=request.POST.get('email'))
                        if new_user == request.user:
                            raise User.DoesNotExist
                        else:
                            return JsonResponse({"message": 'Email is already taken!', "code": False})
                    except User.DoesNotExist:
                        try:
                            new_user2 = User.objects.get(
                                username=request.POST.get('username'))
                            if new_user2 == request.user:
                                raise User.DoesNotExist
                            else:
                                return JsonResponse({"message": 'Username is already taken!', "code": False})
                        except User.DoesNotExist:
                            user.email = request.POST.get('email')
                            user.last_name = request.POST.get('last_name')
                            user.first_name = request.POST.get('first_name')
                            user.username = request.POST.get('username')
                            user.save()
                            return JsonResponse({"message": 'Account updated successfully!', "code": True})
                else:
                    return JsonResponse({"message": 'Some fields are still empty', "code": False})

            if request.POST.get('update_basic'):
                if request.POST.get('bio') != '' and request.POST.get('phone_number') != '' and request.POST.get('role') != '' and request.POST.get('address') != '':
                    user = Profile.objects.get(user=request.user)
                    user.bio = request.POST.get('bio')
                    user.role = request.POST.get('role')
                    user.address = request.POST.get('address')
                    user.phone_number = request.POST.get('phone_number')
                    user.years_of_experiance = request.POST.get(
                        'years_of_experiance')
                    user.save()
                    return JsonResponse({"message": 'Profile updated successfully!', "code": True})
                else:
                    return JsonResponse({"message": 'Some fields are still empty!', "code": False})
        # Update the single user's image
        elif request.FILES['pimage']:
            pik = request.FILES['pimage']
            user = Profile.objects.get(pk=pk)
            user.profile_pik = pik
            user.save()

    return render(request, 'profiles/single_famer.html', context)
