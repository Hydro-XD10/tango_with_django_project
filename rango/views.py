from django.shortcuts import render
from django.http import HttpResponse
from  rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect


def index(request):
    # query the database for a list of all categories currently stored
    # order the categories by the number of likes in descending order
    # retrieve the top 5 only -- or all if less than 5
    category_list = Category.objects.order_by('-likes')[:5]

    # query the database for a list of all pages currently stored
    # order the pages by the number of views in descending order
    # retrieve the top 5 only -- or all if less than 5
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    return render(request, 'rango/index.html', context=context_dict)

def show_category(request,category_name_slug):
    context_dict={}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category

    except  Category.DoesNotExist:

        context_dict['category'] = None
        context_dict['pages'] = None
        
    return render(request, 'rango/category.html', context=context_dict)

def about(request):
    
    return render(request, 'rango/about.html')
 
'''  
    return HttpResponse(
        'Rango says here is the about page.<br />'
        '<a href="/rango/">Index</a>'
    )
'''

def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now that the category is saved,
            # redirect the user back to the index view.
            return redirect('/rango/')
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form,
    # or no form supplied cases.
    return render(request,
                  'rango/add_category.html',
                  {'form': form})

# Create your views here.
