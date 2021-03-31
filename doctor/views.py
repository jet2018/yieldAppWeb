from django.shortcuts import render, get_object_or_404
from profiler.models import Profile
from .models import  Notifications, Reply
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView
from django.forms.models import model_to_dict
from django.core import serializers
from django.contrib.auth.decorators import login_required


class DoctorListView(ListView):
    model = Profile
    context_object_name = 'doctors'
    template_name = "doctor/list_doctors.html"

    def get_queryset( self ):
        return Profile.objects.filter(role = 'dr')

class NotificationsDetailView(DetailView):
    model = Notifications
    context_object_name = 'notification'
    template_name = "notifications/readEmail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = Reply.objects.filter(on = self.object)
        return context

    # def get_queryset( self ):
    #     return Profile.objects.filter(role = 'dr')

@login_required(login_url = '/login/')
def starAdoctor(request):
    if request.is_ajax():
        post = get_object_or_404(Profile, pk = request.GET.get('id'))
        
        if post.stars.filter(id = request.user.id).exists():
            post.stars.remove(request.user)
        else:
           post.stars.add(request.user)
        countNow = post.total_stars
        return JsonResponse({
            "countNow": countNow,
            "result":'ok'
        })


@login_required(login_url = '/login/')
def sendNotification(request):
    if request.is_ajax():
        to = Profile.objects.get(user__id = request.POST.get('id'))
        if to is not None:
            sender = Profile.objects.get(user = request.user)
            body = request.POST.get('body')
            if body == '':
                message = "You can't submit an empty notification"
                return JsonResponse({
                    'message':message,
                    'code': False
                })
            else:
                notify = Notifications(to = to, fro = sender, body = body)
                notify.save()
                message = "Notification sent successfully"
                return JsonResponse({
                    'message':message,
                    'code': True
                })
        else:
            message = "Error fetching this User"
            return JsonResponse({
                    'message':message,
                    'code': False
               })


@login_required(login_url = '/login/')
def replySubmit(request, id):
    if request.is_ajax():
        on = Notifications.objects.get(pk = id)
        if on is not None:
            sender = Profile.objects.get(user = request.user)
            receiver = Profile.objects.get(user = on.fro.user)
            body = request.POST.get('body')
            if body == '':
                message = "You can't submit an empty reply"
                return JsonResponse({
                    'message' : message,
                    'code' : False
                })
            else:
                notify = Reply(on = on, to = receiver, fro = sender, body = body)
                notify.save()
                message = "Repply sent successfully"
                return JsonResponse({
                    'message':message,
                    'code': True,
                }, safe=True)
        else:
            message = "Error fetching this User"
            return JsonResponse({
                    'message':message,
                    'code': False
               })

@login_required(login_url = '/login/')
def deleteReply(request, id):
    if request.is_ajax():
        reply = get_object_or_404(Reply, pk = id, fro__user = request.user)
        deleter = reply.delete()
        if deleter:
            return JsonResponse({'message': "Reply deleted successfully", 'code': True})
        else:
            return JsonResponse({'message': "Reply was not deleted", 'code': False})



@login_required(login_url = '/login/')
def getNotifications(request):
    if request.is_ajax():
        data = request.GET.get('user')
        mydict = {}
        user = get_object_or_404(Profile, pk = data)
        get_count_of_unread_to = Notifications.objects.filter(to__user = request.user, status = False).count()
        get_sent_notifications_count = Notifications.objects.filter(fro__user = request.user,).count()
        get_your_inbox_all = Notifications.objects.filter(to__user = request.user,).count()
        mydict['you_sent_count'] = get_sent_notifications_count
        mydict['you_receive_unread'] = get_count_of_unread_to
        mydict['get_your_inbox_all'] = get_your_inbox_all
        return JsonResponse({'dict':mydict}, safe = False)


@login_required(login_url = '/login/')
def markAllAsRead(request):
    if request.is_ajax():
        if request.GET.get('unread'):
            Notifications.objects.filter(to__user = request.user, status = False).update(status = True)
            return JsonResponse({'message':"All updated", 'code': True})
    return redirect('/doctors/all_notifications')



@login_required(login_url = '/login/')
def DeleteEmail(request):
    if request.is_ajax():
        if request.GET.get('id'):
            Notifications.objects.get(to__user = request.user, pk = request.GET.get('id')).delete()
            return JsonResponse({'message':"Notification deleted successfully", 'code': True})
    return redirect('/doctors/all_notifications')



@login_required(login_url = '/login/')
def DeleteEmailSent(request):
    if request.is_ajax():
        if request.GET.get('id'):
            Notifications.objects.get(fro__user = request.user, pk = request.GET.get('id')).delete()
            return JsonResponse({'message':"Notification deleted successfully", 'code': True})
    return redirect('/doctors/all_notifications')
    

@login_required(login_url = '/login/')
def MarkOneAsRead(request):
    if request.is_ajax():
        if request.GET.get('id'):
            Notifications.objects.filter(to__user = request.user, pk=request.GET.get('id')).update(status = True)
            return JsonResponse({'message':"Updated successfully", 'code': True})
    return redirect('/doctors/all_notifications')


class getAllNotifications(ListView):
    model = Notifications
    context_object_name = 'notifications'
    template_name = "notifications/inbox.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sent'] = Notifications.objects.filter(fro__user = self.request.user)
        context['received'] = Notifications.objects.filter(to__user = self.request.user)
        context['unread'] = Notifications.objects.filter(to__user = self.request.user, status = False)
        return context




@login_required(login_url = '/login/')
def ComposeNotification(request):
    if request.is_ajax():
        body = request.POST.get('body')
        myuser = User.objects.get(email = request.POST.get('email'))
        if myuser is not None:
            to = Profile.objects.get(user = myuser)
            if to is not None:
                fro = Profile.objects.get(user = request.user)
                if fro is not None:
                    new_notification = Notifications.objects.create(to = to, fro = fro, body = body)

                    if new_notification:
                        message = "Notification sent successfully"
                        return JsonResponse({
                                'message':message,
                                'code': True
                            })
                    else:
                        message = "An error occurred and your notification was not sent"
                        return JsonResponse({
                                'message':message,
                                'code': False
                            })
                else:
                    message = "Could not pick the current session, maybe re-login"
                    return JsonResponse({
                            'message':message,
                            'code': False
                        })
            else:
                message = "No profile is associated with the given email"
                return JsonResponse({
                            'message':message,
                            'code': False
                        })
        else:
            message = "No user us associated with the given email"
            return JsonResponse({
                    'message':message,
                    'code': False
                })

    sent = Notifications.objects.filter(fro__user = request.user)
    received = Notifications.objects.filter(to__user = request.user)
    unread = Notifications.objects.filter(to__user = request.user, status = False)
    return render(request, 'notifications/create_notification.html', context={
            'sent': sent,
            'received':received,
            'unread': unread
        })
