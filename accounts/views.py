from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data
            user = authenticate(request,
                                username=date['username'],
                                password=date['password']
                                )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Muvaffaqiyatli login amalga oshirildi!')
                else:
                    return HttpResponse('Sizning profilingiz faol holatda emas!')
            else:
                return HttpResponse('Login va parolda xatolik bor!')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


@login_required
def dashboard_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'pages/user_profile.html', context)


def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                'new_user': new_user,
            }

            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegistrationForm()

    context = {
        'user_form': user_form,
    }
    return render(request, 'account/register.html', context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/register.html'


@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST,
                                       instance=request.user.profile,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'account/edit_profile.html', context)


class EditUserView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }

        return render(request, 'account/edit_profile.html', context)

    def post(self, request):
        user_form = UserEditForm(data=request.POST,
                                 instance=request.user)
        profile_form = ProfileEditForm(data=request.POST,
                                       instance=request.user.profile,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')


class LogoutCustomView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
