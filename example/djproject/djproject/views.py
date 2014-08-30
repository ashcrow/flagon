
from django.http import HttpResponse
from django.conf import settings


def new_index(request):
    return HttpResponse("I am the sweet new index!")


@settings.FEATURE('OLD_INDEX', default=new_index)
def index(request):
    return HttpResponse("I am the goold ol' index.")


def hello(request):
    if settings.FEATURES.is_active('FORMAL_GREETINGS', if_unknown=False):
        return HttpResponse("Good day, sir!")
    else:
        return HttpResponse("Sup, guy?")
