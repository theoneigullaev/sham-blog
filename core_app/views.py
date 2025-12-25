from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout 
# ИСПРАВЛЕНО: UserCreationForm (было UseCreationForm)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.decorators import login_required
from .models import Post
# ИСПРАВЛЕНО: .forms (было .froms)
from .forms import PostForm 

# Регистрация
def register_view(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    
    # ИСПРАВЛЕНО: Исправлен отступ и опечатка request (было rewuest)
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid(): # ИСПРАВЛЕНО: Добавлено двоеточие
            user = form.save()
            # login(request, user) # Можно сразу залогинить пользователя после регистрации
            return redirect('login_view')
    else:
        form = UserCreationForm()
        
    context = {'form': form}
    # ИСПРАВЛЕНО: Точка вместо запятой в "register.html"
    return render(request, "register.html", context)

# Авторизация
def login_view(request):
    if request.user.is_authenticated:
        return redirect('post_list')  

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('post_list') 
    else:
        form = AuthenticationForm()
    
    # ИСПРАВЛЕНО: Ключ 'form' (было 'from')
    context = {'form': form}
    return render(request, "login.html", context)

# Выход
def logout_view(request): # ИСПРАВЛЕНО: Имя функции (было logout_views)
    logout(request)
    return redirect('login_view')

# Список постов
def post_list(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, "posts.html", context)

@login_required(login_url='login_view')
def create_post_view(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    
    # Эти строки должны быть ВНУТРИ функции (4 пробела от края)
    context = {
        'form': form,
        'title': 'Создать запись'
    }
    
    return render(request, 'post_form.html', context)

@login_required(login_url='login_view')
def update_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    context = {
        'form': form
    }
    return render(request, "post_form.html", context)


@login_required(login_url='login_view')
def delete_post_view(request, pk):
    # Все эти строки должны иметь одинаковый отступ (4 пробела)
    post = get_object_or_404(Post, pk=pk, user=request.user)

    if request.method == "POST":
        # Внутри if — еще один уровень отступа (8 пробелов)
        post.delete()
        return redirect('post_list') 

    context = {
        'post': post
    }   
    return render(request, "delete.html", context)