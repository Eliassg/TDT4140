from django.shortcuts import render, get_object_or_404

from .models import Post, get_post_by_id, get_comments_by_post, Emne, get_posts_by_emne, ReportPost, Comment, ReportComment, get_comment_by_id

# Create your views here.

# Imports for register of user (Baard)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import (
    SignUpForm, 
    EditProfileForm,
    EditUserProfileForm
 ) #UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import RedirectView

# laster følgende inn for bildefilopplasting
from django.core.files.storage import FileSystemStorage

# imports for userprofile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


# Methods for registry of user with "SignUpForm".
def index(request):
    emneListe = Emne.objects.all()
    posts = Post.objects.order_by("submission_time").reverse()[:5]
    context = {'emneListe': emneListe, 'posts':posts}
    return render(request, 'index.html', context)


def registerPage(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Bruker ble laget for " + user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Brukernavn eller passord er feil")
    
    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect("login")
        

def emneSide(request, id):
    emne = get_object_or_404(Emne, pk=id)
    emneListe = Emne.objects.all()
    posts = get_posts_by_emne(emne)
    context = {'emneListe': emneListe, 'emne': emne, 'posts':posts}
    return render(request, 'emner.html', context)


def userpost(request, post_id):
    post = get_post_by_id(post_id)
    comments = get_comments_by_post(post_id).order_by("submission_time").reverse()
    if request.method == "POST":
        if request.POST.get("deleteValue") == "deleteYes":
            post.delete()
            return redirect("index")
        if request.POST.get("reportPostValue") == "reportPostYes":
            report_post = ReportPost()
            report_post.author = request.user
            report_post.post = get_post_by_id(post_id)
            report_post.save()
        if request.POST.get("reportCommentValue") == "reportCommentYes":
            report_comment = ReportComment()
            report_comment.author = request.user
            report_comment.comment = get_comment_by_id(request.POST.get("commentID"))
            report_comment.save()
        if request.POST.get("commentPostValue") == "commentYes":
            post = get_post_by_id(post_id)
            post.add_comment(request.POST.get("commentText"), request.user)
            return redirect(request.path_info)
    return render(request, 'postView.html', {'post': post, 'comments': comments, 'user':  request.user})

#klasse for å aktivere likes
class PostLikeToggle(RedirectView):
    #funksjonen sørger for redirect tilbake til posten. For at siden ikke skal laste inn på nytt
    #   må vi bruke vi bruke JS ens. 
    def get_redirect_url(self, *args, **kwargs):
        post_id = self.kwargs.get("post_id")
        print(post_id)
        obj = get_post_by_id(post_id)
        url_ = obj.get_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_


def postCreation(request):
    emner = Emne.objects.all()
    if request.method == "POST":
        post = Post()
        post.author = request.user
        post.title = request.POST.get("postTitle")
        post.text = request.POST.get("postDesc")
        emneinput = request.POST.get("emnenavn")
        post.emne = Emne.objects.get(emnenavn=emneinput)
        post.save()
        return redirect("/forumApp/userpost/"+str(post.id))
    return render(request, 'postCreation.html', {'emner': emner})




# Funksjon for at brukere skal kunne slette sin egen bruker.
def delete_user(request, username):
    context = {'user': request.user}
    try:
        u = User.objects.get(username=username)
        u.delete()
        context['msg'] = 'The user is deleted.'       
    except User.DoesNotExist: 
        context['msg'] = 'User does not exist.'
    except Exception as e: 
        context['msg'] = e.message

    return render(request, 'register.html', context=context)

# Fysisk knapp til sletting av bruker, samt dobbeltsjekk om sletting
def delete_user_confirm(request):
    return render(request, 'deleteUser.html')

# Side for visning av søkeresultat
def show_search_result(request):
    context = {}
    emneListe = Emne.objects.all()      # liste over alle emner
    queryset_list = Post.objects.all()  # liste over alle poster

    query = request.GET.get("q")        # søkeord fra metode i template
    sokeord = str(query)
    if query:
        queryset_list = queryset_list.filter(title__icontains=query) #filtrerer de postene som inneholder søkeord

    context = {                         # innhold som kan hente ut i searchresult.html
        'emneListe': emneListe,
        'object_list': queryset_list,
        'search_word': sokeord 
    }
    return render(request,'searchresult.html', context=context)


# for at brukere skal kunne se sin egen og andres profil
def view_profile(request, username):
    user = User.objects.get(username=username)
    context = {'user': user, 'profile_owner': user==request.user}
    return render(request, 'account/profile.html', context) #args)

#funkjson for at brukere skal kunne redigere profilsiden sin
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        userprofile_form = EditUserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and userprofile_form.is_valid():
            user_form.save() # lagrer til brukeren
            userprofile_form.save() # lagrer til brukeren
            return redirect('view_profile', username=request.user.username) # sender tilbake til prfoilsiden når endringen er ferdig

    else:
        user_form = EditProfileForm(instance=request.user)
        userprofile_form = EditUserProfileForm(instance=request.user)

        args = {'user_form': user_form, 'userprofile_form': userprofile_form, 'user':request.user}
        return render(request, 'account/edit_profile.html', args)

# funkjson for at brukeren skal kunne endre passord
def change_password(request):
    # når brukeren vil lagre endringene den har fylt inn (altså oppdatere passord)
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('view_profile', username=request.user.username) # sender tilbake til prfoilsiden når endringen er ferdig
        else:
            return redirect('/forumApp/profile/change-password') # hvis det ikke er valid blir de sendt tilbake til samme side
    
    # når brukeren bare går inn på siden
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form, 'user': request.user}
        return render(request, 'account/change_password.html', args)
