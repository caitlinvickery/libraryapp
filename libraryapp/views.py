from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Activity
from django.db import models

# Temporary hardcoded users
USERS = {
    "admin": {"password": "adminpass", "role": "admin"},
    "user": {"password": "userpass", "role": "user"},
}

# Home View
def home(request):
    username = request.user.username if request.user.is_authenticated else None

    all_books = Book.objects.all()

    recommended_books = all_books[:3]
    featured_books = all_books[3:6]

    # Get recent activities (logged-in user + others who interacted with user's books)
    if request.user.is_authenticated:
        activities = Activity.objects.filter(
            models.Q(user=request.user) | models.Q(book__created_by=request.user.username)
        ).order_by('-timestamp')[:6]
    else:
        activities = Activity.objects.none()

    return render(
        request,
        "libraryapp/home.html",
        {
            "username": username,
            "recommended_books": recommended_books,
            "featured_books": featured_books,
            "activities": activities,  # Pass to template
        },
    )

# Login View
from django.contrib.auth import authenticate, login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, "libraryapp/login.html")

# Logout View
def logout_view(request):
    # Clear the session to log the user out
    request.session.flush()
    # Redirect to the home page after logging out
    return redirect("home")

from .models import Review
# Book Detail View
def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    reviews = Review.objects.filter(book=book).order_by('-created_at')  # newest first

    return render(request, "libraryapp/details.html", {
        "book": book,
        "reviews": reviews,
    })

#Add Book View
from .models import Book
from django.contrib import messages

def add_book(request):
    if request.method == "POST":
        # Get data from form
        title = request.POST.get("title")
        author = request.POST.get("author")
        genre = request.POST.get("genre")
        description = request.POST.get("description")
        image = request.FILES.get("book-image")
        created_by = request.user.username

        # Create new book entry
        book = Book(
            title=title,
            author=author,
            genre=genre,
            description=description,
            created_by=created_by,
        )

        if image:
            book.image = image
        else:
            book.image = "book0.jpg"

        book.save()

        messages.success(request, f'"{book.title}" was successfully added.')

        Activity.objects.create(
            user=request.user,
            action_type="add_book",
            book=book,
            description=f"added a new book <a href='/books/{book.id}/'>{book.title}</a>."
        )
        return redirect("detail", id=book.id)

    return render(request, "libraryapp/add.html", {"username": request.user.username})

#Book List View
def book_list(request):
    query = request.GET.get("query", "")
    sort_by = request.GET.get("sort", "title")  # default to title

    # Only allow known sort fields
    if sort_by not in ["title", "author"]:
        sort_by = "title"

    books = Book.objects.filter(title__icontains=query).order_by(sort_by)

    return render(request, "libraryapp/list.html", {
        "books": books,
        "current_sort": sort_by,
    })

#Edit Book View
def edit_book(request, id):
    # Get the book from the database or return 404
    book = get_object_or_404(Book, id=id)

    old_title = book.title
    old_description = book.description

    if request.method == "POST":
        # Update the book with new values
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.genre = request.POST.get("genre")
        book.description = request.POST.get("description")
        book.save()

        # Compare old and new title
        if old_title != book.title:
            Activity.objects.create(
                user=request.user,
                action_type="edit_title",
                book=book,
                description=f"changed the title of <a href='/books/{book.id}/'>{old_title}</a> to <strong>{book.title}</strong>."
            )

        # Compare old and new description
        if old_description != book.description:
            Activity.objects.create(
                user=request.user,
                action_type="edit_description",
                book=book,
                description=f"edited the description of <a href='/books/{book.id}/'>{book.title}</a>."
            )

        messages.info(request, f'"{book.title}" was updated.')
        return redirect("detail", id=book.id)

    return render(request, "libraryapp/edit.html", {"book": book})


# Delete Book View
def delete_book(request, id):
    # Only allow deletion via POST and by admin users
    if request.method == "POST" and hasattr(request.user, "profile") and request.user.profile.role == "admin":
        book = get_object_or_404(Book, id=id)
        title = book.title
        book_title = book.title

        Activity.objects.create(
        user=request.user,
        action_type="delete_book",
        description=f"deleted the book titled <strong>{book_title}</strong>."
    )
        book.delete()

        messages.warning(request, f'"{title}" was deleted.')
        return redirect("list")

    return HttpResponse("Unauthorized", status=403)

from django.http import JsonResponse
# Book availability (Ajax GET request)
def book_availability(request, id):
    # Returns availability status and a fixed location based on book ID
    available = (id % 2 == 0)
    location = "Herndon"

    return JsonResponse({
        "available": available,
        "location": location
    })

from django.views.decorators.csrf import csrf_exempt

#Book rating (Ajax POST)
@csrf_exempt  
def rate_book(request, id):
    if request.method == "POST":
        try:
            # Fetch the book from the database
            book = Book.objects.get(id=id)
            
            # Get the new rating value from the POST data
            new_rating = int(request.POST.get("rating", 0))

            # Clamp rating between 1–5
            new_rating = max(1, min(new_rating, 5))

            book.rating = new_rating
            book.save()

            return JsonResponse({"status": "success", "new_rating": book.rating})
        except Book.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Book not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

from .forms import UserRegisterForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'libraryapp/register.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

@login_required
def manage_roles(request):
    if not request.user.profile.role == 'admin':
        return HttpResponse("Unauthorized", status=403)

    users = User.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('new_role')

        user = get_object_or_404(User, id=user_id)
        old_role = user.profile.role
        user.profile.role = new_role
        user.profile.save()

        if old_role != new_role:
            # Activity for the user whose role was changed
            Activity.objects.create(
                user=user,
                action_type="change_role",
                description=f'Your role was changed to <strong>{new_role}</strong> by <a href="/profile/{request.user.username}/">{request.user.username}</a>.'
            )

            # Activity for the admin who made the change
            Activity.objects.create(
                user=request.user,
                action_type="change_role",
                description=f'You changed <a href="/profile/{user.username}/">{user.username}</a>\'s role to <strong>{new_role}</strong>.'
            )

        return redirect('manage_roles')

    return render(request, 'libraryapp/manage_roles.html', {'users': users})

from django.contrib.auth.models import User
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

def view_profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    # Get only that user's activities
    activities = Activity.objects.filter(user=profile_user).order_by('-timestamp')[:8]

    return render(request, 'libraryapp/profile.html', {
        'profile_user': profile_user,
        'activities': activities, 
    })

@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)

    # Only allow user to edit themselves OR admins to edit others
    if request.user != user and request.user.profile.role != 'admin':
        return HttpResponse("Unauthorized", status=403)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save(user)
            return redirect('view_profile', username=user.username)
    else:
        form = ProfileForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'favorite_genre': user.profile.favorite_genre,
        })

    return render(request, 'libraryapp/edit_profile.html', {'form': form, 'profile_user': user})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def add_review(request, id):
    if request.method == "POST" and request.user.is_authenticated:
        content = request.POST.get('content')
        rating = int(request.POST.get('rating', 0))

        if content and rating:
            book = get_object_or_404(Book, id=id)
            review = Review.objects.create(
                book=book,
                user=request.user,
                content=content,
                rating=rating 
            )
            Activity.objects.create(
                user=request.user,
                action_type="add_review",
                book=book,
                description=f'left a review on <a href="/books/{book.id}/">{book.title}</a>.'
            )
            return JsonResponse({
                "status": "success",
                "username": request.user.username,
                "content": review.content,
                "rating": review.rating, 
                "created_at": review.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "review_id": review.id
            })
        return JsonResponse({"error": "Missing content or rating"}, status=400)
    return JsonResponse({"error": "Unauthorized"}, status=401)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def delete_review(request, id):
    if request.method == "POST":
        try:
            review = Review.objects.get(id=id)
            # Check permissions
            if request.user == review.user or request.user.profile.role == 'admin':
                review.delete()
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)
        except Review.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Review not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@csrf_exempt
def edit_review(request, id):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            review = Review.objects.get(id=id)
            if review.user == request.user or request.user.profile.role == 'admin':
                review.content = request.POST.get("content")
                review.rating = int(request.POST.get("rating"))
                review.save()
                return JsonResponse({"status": "success", "new_rating": review.rating})
            else:
                return JsonResponse({"status": "error", "message": "Permission denied"}, status=403)
        except Review.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Review not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
