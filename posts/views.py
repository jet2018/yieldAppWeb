from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView, DetailView
from .models import Post, postComment, Commentreply
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        myposts = Post.objects.all()
        return render(request, 'posts/all_posts.html', {'posts': myposts})
    else:
        return render(request, 'auths/index.html')


@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return redirect("/")


def login(request):
    if request.is_ajax():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            result = "Login successfull"
            classNow = "success"
        else:
            result = "No member is associated with the given credentials"
            classNow = "danger"
        return JsonResponse({"result": result, "class": classNow}, status=200)
    return render(request, 'auths/login.html')


def register(request):
    if request.is_ajax():
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        password2 = request.POST.get('password2')

        if username == "" or email == "" or password1 == "" or password2 == "" or fname == "" or lname == "":
            result = "Some form fields are still empty"
            classNow = 'danger'
        elif password1 != password2:
            result = "Passwords are not matching"
            classNow = 'danger'
        else:
            if User.objects.filter(username=username).exists():
                result = "The username is already taken"
                classNow = 'warning'
            elif User.objects.filter(email=email).exists():
                result = "The email is associated with some other account"
                classNow = 'warning'
            else:
                user = User.objects.create_user(username=username, password=password2, email=email, first_name=fname,
                                                last_name=lname)
                user.save()
                result = "Account created successfully, you can now login"
                classNow = 'success'

        return JsonResponse({"result": result, "class": classNow}, status=200)
    return render(request, 'auths/register.html')


def forgot(request):
    return render(request, 'auths/forgot_password.html')


def recover(request):
    return render(request, 'auths/recover_password.html')

# class Posts(TemplateView):
# 	# model = Post
# 	template_name = 'posts/all_posts.html'

# 	def get_context_data(self, *args, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		context['myposts'] = Post.objects.all()
# 		return context


@login_required(login_url='/login/')
def post_a_Post(request):
    if request.method == 'POST' or request.is_ajax():
        Image = request.FILES.get('image')
        video = request.FILES.get('video')
        body = request.POST.get('body')
        title = request.POST.get('title')
        message = ""
        status = False
        if Image is None and video is None and body == '' and title == '':
            message = "Are you submitting an empty post?"
            status = False
        elif Image is not None and video is not None:
            mypost = Post(title=title, body=body,
                          Image=Image, posted_by=request.user)
            mypost.save()
            message = "Only your image was attached."
            status = True
        # elif Image != '' and title != '' and body != '':
        #     mypost = Post(title=title, body=body,
        #                   Image=Image, posted_by=request.user)
        #     mypost.save()
        #     status = True
        # elif video != '' and title != '' and body != '':
        #     mypost = Post(title=title, body=body,
        #                   video=video, posted_by=request.user)
        #     mypost.save()
        #     status = True
        else:
            mypost = Post(title=title, body=body, video=video,
                          Image=Image, posted_by=request.user)
            mypost.save()
            message = "Uploaded successfully"
            status = True
    return JsonResponse({"status": status, "message": message})


@ login_required(login_url='/login/')
def likeapost(request):
    if request.is_ajax():
        post = get_object_or_404(Post, pk=request.GET.get('id'))

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        countNow = post.total_likes
        return JsonResponse({
            "countNow": countNow,
            "result": 'ok'
        })


@ login_required(login_url='/login/')
def deletepost(request):
    if request.is_ajax():
        post = Post.objects.get(pk=request.GET.get('id'))
        if post.posted_by == request.user:
            mydel = post.delete()
            return JsonResponse({
                "result": 'ok'
            })
        else:
            return JsonResponse({
                "result": 'no'
            })


def AddComment(request, pk):
    if request.method == 'POST':
        if request.is_ajax():
            try:
                myComment = Post.objects.get(pk=pk)
                comment_body = request.POST.get('body')
                comment_fro = request.user
                if comment_body == "":
                    result = "The comment you submitted seems empty!"
                    classNow = 'danger'
                else:
                    mycomm = postComment.objects.create(
                        comment_to=myComment,
                        comment_body=comment_body,
                        comment_by=comment_fro
                    )

                    if mycomm:
                        num = Post.objects.get(pk=pk).total_comments
                        result = "You commented successfully!"
                        classNow = 'success'
                    else:
                        result = "An error occured and your comment was not added!"
                        classNow = 'error'
            except myComment.DoesNotExist:
                result = "The post you are trying to comment on no-longer exists!"
                classNow = 'danger'

    return JsonResponse({"result": result, "class": classNow, "new_num": num}, status=200)


@ login_required(login_url='/login/')
def likeacomment(request):
    if request.is_ajax():
        comment = get_object_or_404(postComment, pk=request.GET.get('id'))

        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)

        countNow = comment.total_likes
        return JsonResponse({
            "countNow": countNow,
            "result": 'ok'
        })


@ login_required(login_url='/login/')
def deleteacomment(request):
    if request.is_ajax():
        post = get_object_or_404(postComment, pk=request.GET.get('id'))
        try:
            post = postComment.objects.get(pk=request.GET.get('id'))
            mydel = post.delete()
            if mydel:
                mypostNow = Post.objects.get(pk=request.GET.get('post_id'))
                if mypostNow:
                    countNow = mypostNow.total_comments
                    print(countNow)
                    return JsonResponse({
                        "countNow": countNow,
                        "result": 'ok'
                    })
                else:
                    return JsonResponse({
                        "result": 'no'
                    })
            else:
                return JsonResponse({
                    "result": 'no'
                })
        except post.DoesNotExist:
            return JsonResponse({
                "result": 'no'
            })


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/single_post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = postComment.objects.filter(
            comment_to=self.object)
        return context

    # def post()
