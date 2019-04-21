from .models import User, Client


def users(request):
    context = {}
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        context['name'] = user.first_name
        context['surname'] = user.last_name

    return context


def account(request):
    context = {}
    if request.user.is_authenticated:
        username = request.user.username
        client = Client.objects.get(username=username)
        context['accounts'] = client.accounts.all()

    return context
