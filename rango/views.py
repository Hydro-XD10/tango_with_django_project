from django.shortcuts import render
from django.http import HttpResponse
from  rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from rango.forms import PageForm
from django.urls import reverse
from rango.forms import UserForm,UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout



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


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # you cannot add a page to a category that does not exist...
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


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
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()

            return redirect(reverse('rango:show_category',
                                    kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


def register(request):
    # A boolean value for telling the template
    # whether the registration was successful
    # Set to False initially. Code changes value to
    # True when registration succeeds
    registered = False

    # If it's a HTTP POST, we're interested in processing form data
    if request.method == 'POST':
        # Attempt to grab information from the raw form information
        # Note that we make use of both UserForm and UserProfileForm
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True

        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)

    else:
        # Not a HTTP POST, so we render our using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'rango/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})

def user_login(request):
    # if the request is a http post, try to pull out the relevant information.
    if request.method == 'POST':
        # gather the username and password provided by the user.
        # this information is obtained from the login form.
        # we use request.post.get('<variable>') as opposed
        # to request.post['<variable>'], because the
        # request.post.get('<variable>') returns none if the
        # value does not exist, while request.post['<variable>']
        # will raise a keyerror exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # use django's machinery to attempt to see if the username/password
        # combination is valid - a user object is returned if it is.
        user = authenticate(username=username, password=password)

        # if we have a user object, the details are correct.
        # if none (python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # is the account active? it could have been disabled.
            if user.is_active:
                # if the account is valid and active, we can log the user in.
                # we'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                # an inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # bad login details were provided. so we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    # the request is not a http post, so display the login form.
    # this scenario would most likely be a http get.
    else:
        # no context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html')


'''
def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")
'''



from django.contrib.auth.decorators import login_required


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")



@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take them back to the homepage.
    return redirect(reverse('rango:index'))
