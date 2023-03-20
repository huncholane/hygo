from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    print(request.user)
    return render(request, 'home/index.html')


def login_view(request):
    if request.method == 'POST':
        if None in [request.POST['username'], request.POST['password']]:
            user = None
        user = authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'home/login.html', {
                'login_error': 'User not found.'
            })
        else:
            login(request, user)
            return redirect('..')
    print('wtf')
    return render(request, 'home/login.html')


def register(request):
    if request.method == 'POST':
        data = request.POST
        required = {'username', 'password', 'email',
                    'password_confirm', 'first_name', 'last_name'}
        missing = required.difference(set(data))
        if len(missing) > 0 or data['password'] != data['password_confirm']:
            return render(request, 'home/register.html', {
                'error_message': 'Missing '+', '.join(missing)+' password not the same.'
            })
        if User.objects.filter(username=data['username']).exists():
            return render(request, 'home/register.html', {
                'error_message': 'User already exists.'
            })
        user = User.objects.create_user(
            data['username'], data['email'], data['password'])
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()
        login(request, user)
        return redirect('/')
    return render(request, 'home/register.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def favicon(request):
    return redirect('/static/favicons/favicon.ico')
