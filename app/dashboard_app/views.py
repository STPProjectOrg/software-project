from django.shortcuts import render

# Create your views here.
def dashboard(request):
    data = {'value': 0}
    return render(request, 'dashboard_app/dashboard.html', context=data)