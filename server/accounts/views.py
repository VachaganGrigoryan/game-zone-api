from django.shortcuts import render


def dashboard(request):
    return render(request, "users/dashboard.html")


def permission_denied_handler(request):
    from django.http import HttpResponse
    return HttpResponse('you have no permissions!')
