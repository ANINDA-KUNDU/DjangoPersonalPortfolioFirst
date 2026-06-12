from django.shortcuts import render
from .models import Work
# Create your views here.

def home(request):
    works = Work.objects.order_by('-id')[:5]
    return render(request, 'core/home.html', {'works': works })

def contact(request):
    return render(request, 'core/contact.html')

def work(request):
    works = Work.objects.all()
    return render(request, 'core/work.html', { 'works': works } )

def about_me(request):
    return render(request, 'core/about_me.html')