from django.shortcuts import render, get_object_or_404
from .models import Profile
from posts.models import Post
from django.contrib.auth.models import User
from django.http import JsonResponse
from doctor.models import Notifications
from django.views.generic import  ListView, DetailView
from .forms import ImageUploadForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required

# Create your views here.
		
class UserListView(ListView):
    model = Profile
    context_object_name = 'users'
    template_name = "profiles/all_users.html"

    def get_queryset( self ):
        return Profile.objects.all()


@login_required(login_url = '/login/')
def UpdateProfileImage(request):
    if request.method == 'POST':
        myImage = request.FILES['pimage']
        myprofile = get_object_or_404(Profile, user = request.user)
        myprofile.profile_pik = myImage
        myprofile.save()

    return redirect('profile:profile_for')


# get a single user
@login_required(login_url = '/login/')
def SingleUser(request, pk):
    context = {} 
    # form = ImageUploadForm()
    context['profile'] = Profile.objects.get(pk = pk)
    context['posts'] = Post.objects.filter(posted_by = request.user)
    context['received_notifications'] = Notifications.objects.filter(to__user = request.user)
    context['sent_notifications'] = Notifications.objects.filter(fro__user = request.user)

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
                    matchcheck= check_password(request.POST.get('password1'), current_password)
                    if matchcheck:
                        user = User.objects.get(pk = request.user.id)
                        user.set_password(request.POST.get('password2'))
                        user.save()
                        return JsonResponse({"message": 'Password updated successfully, logging you out!', "code": True})
                    else: 
                        return JsonResponse({"message": 'No account is associated with the given password!', "code": False})
                else:
                    return JsonResponse({"message": 'Some fields are still empty', "code": False})

            if request.POST.get('update_advanced'):
                if request.POST.get('email') != '' and request.POST.get('last_name') != '' and request.POST.get('username') != '' and request.POST.get('first_name') != '':
                    user = User.objects.get(pk = request.user.id)
                    try:
                        new_user = User.objects.get(email = request.POST.get('email'))
                        if new_user ==  request.user:
                            raise User.DoesNotExist
                        else:
                            return JsonResponse({"message": 'Email is already taken!', "code": False})
                    except User.DoesNotExist:
                        try:
                            new_user2 = User.objects.get(username = request.POST.get('username'))
                            if new_user2 ==  request.user:
                                raise User.DoesNotExist
                            else:
                                return JsonResponse({"message": 'Username is already taken!', "code": False})
                        except User.DoesNotExist:
                            user.email = request.POST.get('email')
                            user.last_name = request.POST.get('last_name')
                            user.first_name =request.POST.get('first_name')
                            user.username =request.POST.get('username')
                            user.save()
                            return JsonResponse({"message": 'Account updated successfully!', "code": True})
                else:
                    return JsonResponse({"message": 'Some fields are still empty', "code": False})
                    
            if request.POST.get('update_basic'):
                if request.POST.get('bio') != '' and request.POST.get('phone_number') != '' and request.POST.get('role') != '' and request.POST.get('address') != '':
                    user = Profile.objects.get(user = request.user)
                    user.bio = request.POST.get('bio')
                    user.role = request.POST.get('role')
                    user.address = request.POST.get('address')
                    user.phone_number = request.POST.get('phone_number')
                    user.years_of_experiance = request.POST.get('years_of_experiance')
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


