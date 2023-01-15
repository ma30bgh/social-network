from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm, EditUserForm
from django.contrib.auth import views as auth_views
#as auth_views gozashtim ke esm hashon ghati nashe
from  django.urls import reverse_lazy
from  .models import Relation


class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    # dispatch ghabl baghiye ejra mishe masalan inja check mikone ke karbar az tarigh url natone vared she
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            messages.success(request, 'Todo registered successfully', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):   #baraye inke vaghti login mikone bere be hamon safe k darkhast login dade
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                if self.next:
                    return redirect(self.next)  #setup ro bala neveshtim barash
                return redirect('home:home')
            messages.error(request, 'Error', 'warning')
        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you are logout successfully', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        #user = User.objects.get(pk=user_id)
        posts = user.posts.all()  #related_name='posts' --> models
        #posts = Post.objects.filter(user=user)
        # agar bekhaym baraye filter ham hamin karo konim az in ravash estefade mikonim
        #posts = get_list_or_404(Post, user = user)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, 'account/profile.html', {'user': user, 'posts': posts, 'is_following': is_following})


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/reset_password_form.html'
    success_url = reverse_lazy('account:reset_password_done')
    email_template_name = 'account/reset_password_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/reset_password_done.html'


class UserPasswordConfirmView (auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView (auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'

class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user= user)
        if relation.exists():
            messages.error(request, 'you are already following this user', 'danger')
        else:
            #Relation.objects.create(from_user=request.user, to_user= user)  --> ravash1 --> create dar khodesh save dare
            Relation(from_user=request.user, to_user= user).save()  #ravesh2
            messages.success(request, 'you followed this user', 'success')
        return redirect('account:user_profile', user.id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user= user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'you unfollowed this user', 'success')
        else:
            messages.error(request, 'you are not following this user', 'danger')
        return redirect('account:user_profile', user.id)


class EditUserView(LoginRequiredMixin, View):
    form_class = EditUserForm

    def get(self,request):
        form = self.form_class(instance=request.user.profile, initial={'email':request.user.email})
        return render(request,'account/edit_profile.html', {'form':form})

    def post(self,request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'profile edited', 'success')
        return redirect('account:user_profile', request.user.id)

