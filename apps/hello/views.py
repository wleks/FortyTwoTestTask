from django.shortcuts import render

from .models import Person


def home_page(request):
    context = {}
    person = Person.objects.first()
    context['person'] = person
    return render(request, 'home.html', context)
