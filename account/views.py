from django.shortcuts import render, redirect, reverse
from account.forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse("main"))
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse("main"))
            else:
                form.add_error(None, "입력한 자격증명에 해당하는 사용자가 없습니다.")
        return render(request, "account/login.html", {"form": form})
    else:
        form = LoginForm()
        return render(request, "account/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect(reverse("main"))

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("main"))
    else:
        form = SignUpForm()
    return render(request, "account/signup.html", {"form": form})
