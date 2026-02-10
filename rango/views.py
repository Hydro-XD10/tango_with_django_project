from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict={'boldmessage':'Crunchy, creamy, cookie, candy, cupcake!'} ## Construct a dictionary to pass to the template engine as its context.
# Note the key boldmessage matches to {{ boldmessage }} in the template!

    return render(request,'rango/index.html',context=context_dict)## Return a rendered response to send to the client.
# We make use of the shortcut function to make our lives easier.
# Note that the first parameter is the template we wish to use.

def about(request):
    
    return render(request, 'rango/about.html')
 
'''  
    return HttpResponse(
        'Rango says here is the about page.<br />'
        '<a href="/rango/">Index</a>'
    )
'''
# Create your views here.
