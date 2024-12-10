from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate,login,logout
from datetime import date, timedelta

from .models import Author, Book, Rental, Genre, Publication, Subscription,  Rental
from .forms import MyLoginForm, UserRegistrationForm ,AddAuthor,AddBook ,AddGenre ,AddPublication, SubscriptionForm, UpgradeSubscriptionForm, RentBookForm
# Create your views here.

def Index(request):
    return render(request,'home.html')
    #return HttpResponse("Welcome")
def user_login(request):
    if request.method == 'POST':
        #we will be getting username and passwords through
        login_form= MyLoginForm(request.POST)
        if login_form.is_valid():
            cleaned_data= login_form.cleaned_data
            auth_user= authenticate(
                request,
                username=cleaned_data['username'],
                password=cleaned_data['password']
                )
            if auth_user is not None:
                login(request, auth_user)
                #get user's role
                group= auth_user.groups.first()
                group_name= group.name if group else "No Group"
                request.session['group_name']= group_name
                return redirect('home_path')
            else:
                return HttpResponse('Not Authenticated')
    else:
        login_form=MyLoginForm()
    return render(request, 'useraccount/user_login.html',{'login_form': login_form})

def custom_logout(request):
    logout(request) #destroy all the session id for a particular user
    return redirect('login')

def register(request):
    if request.method == 'POST':
        #we will be getting username and password through POST
        user_req_form= UserRegistrationForm(request.POST)
        if user_req_form.is_valid():
            #create the form, but will not save it
            new_user= user_req_form.save(commit=False)
            #set the password after validation
            #checking password == confirm password
            #password value is assigned to password field
            new_user.set_password(
                #using set_password()
                user_req_form.cleaned_data['password'])
            new_user.save() #save to db
            return render(request, 'useraccount/register_done.html',{'user_req_form':user_req_form})
    else:
        user_req_form= UserRegistrationForm()
    return render(request, 'useraccount/register.html',{'user_req_form':user_req_form})


#Decorator for role-based access
def role_required(roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.groups.filter(name__in=roles).exists():
                return view_func(request, *args, **kwargs)
            return redirect('login')
        return _wrapped_view
    return decorator

# Admin Dashboard
@login_required
@role_required(['Admin'])
def admin_dashboard(request):
    books = Book.objects.all()
    return render(request, 'admin_dashboard.html', {'books': books})

# User Dashboard
@login_required
@role_required(['User'])
def user_dashboard(request):
    rentals = Rental.objects.filter(user=request.user)
    return render(request, 'useraccount/user_dashboard.html', {'rentals': rentals})


# Book Views
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def book_create(request):
    if request.method == 'POST':
        form = AddBook(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = AddBook()
    return render(request, 'books/book_form.html', {'form': form})

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = AddBook(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = AddBook(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')

# Author Views
def author_list(request):
    authors = Author.objects.all()
    return render(request, 'authors/author_list.html', {'authors': authors})

def author_create(request):
    if request.method == 'POST':
        form = AddAuthor(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AddAuthor()
    return render(request, 'authors/author_form.html', {'form': form})

def author_update(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        form = AddAuthor(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AddAuthor(instance=author)
    return render(request, 'authors/author_form.html', {'form': form})

def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    author.delete()
    return redirect('author_list')

# Genre Views
def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'genres/genre_list.html', {'genres': genres})

def genre_create(request):
    if request.method == 'POST':
        form = AddGenre(request.POST)
        if form.is_valid():
            form.save()
            return redirect('genre_list')
    else:
        form = AddGenre()
    return render(request, 'genres/genre_form.html', {'form': form})

def publication_list(request):
    publications = Publication.objects.all()
    return render(request, 'publications/publication_list.html', {'publications': publications})

def publication_create(request):
    if request.method == 'POST':
        form = AddPublication(request.POST)
        if form.is_valid():
            form.save()
            return redirect('publication_list')
    else:
        form = AddPublication()
    return render(request, 'publications/publication_form.html', {'form': form})

def publication_update(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    if request.method == 'POST':
        form = AddPublication(request.POST, instance=publication)
        if form.is_valid():
            form.save()
            return redirect('publication_list')
    else:
        form = AddPublication(instance=publication)
    return render(request, 'publications/publication_form.html', {'form': form})

def publication_delete(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    publication.delete()
    return redirect('publication_list')

def browse(request):
    books = Book.objects.select_related('author', 'genre', 'publication').all()
    authors = Author.objects.all()
    genres = Genre.objects.all()
    publications = Publication.objects.all()

    return render(request, 'browse.html', {
        'books': books,
        'authors': authors,
        'genres': genres,
        'publications': publications
    })


@login_required
def subscribe_view(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            return redirect('view_subscription')
    else:
        form = SubscriptionForm()
    return render(request, 'useraccount/subscribe.html', {'form': form})

@login_required
def view_subscription(request):
    subscription = Subscription.objects.filter(user=request.user).last()
    return render(request, 'useraccount/view_subscription.html', {'subscription': subscription})

@login_required
def subscription_list(request):
    subscriptions = Subscription.objects.all()
    return render(request, 'useraccount/subscription_list.html', {'subscriptions': subscriptions})




def upgrade_subscription(request):
    if request.method == 'POST':
        form = UpgradeSubscriptionForm(request.POST)
        if form.is_valid():
            new_plan = form.cleaned_data['plan']
            subscription = Subscription.objects.filter(user=request.user).last()
            if subscription:
                subscription.plan = new_plan
                subscription.save()
                return redirect('view_subscription')
    else:
        form = UpgradeSubscriptionForm()
    return render(request, 'useraccount/upgrade_subscription.html', {'form': form})


@login_required
def rent_book(request):
    if request.method == 'POST':
        form = RentBookForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.user = request.user
            # Ensure rental limit
            subscription = Subscription.objects.filter(user=request.user).last()
            if not subscription:
                form.add_error(None, "No active subscription found.")
            else:
                active_rentals = Rental.objects.filter(user=request.user, status='Borrowed').count()
                if active_rentals >= subscription.max_rentals:
                    form.add_error(None, "Rental limit exceeded for your membership plan.")
                else:
                    rental.rental_date = date.today()
                    rental.save()
                    return redirect('view_rentals')
    else:
        form = RentBookForm()
    return render(request, 'useraccount/rent_book.html', {'form': form})




def rental_list(request):
    rentals = Rental.objects.all()
    return render(request, 'useraccount/rental_list.html', {'rentals': rentals})
