from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("books/", views.book_list, name="list"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("books/<int:id>/", views.book_detail, name="detail"),
    path("books/add/", views.add_book, name="add"),
    path("books/<int:id>/edit/", views.edit_book, name="edit"),
    path("books/<int:id>/delete/", views.delete_book, name="delete"),
    path("api/book-availability/<int:id>/", views.book_availability, name="book_availability"),
    path("api/rate-book/<int:id>/", views.rate_book, name="rate_book"),
    path('register/', views.register, name='register'),
    path('manage-roles/', views.manage_roles, name='manage_roles'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
        path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='libraryapp/password_change.html',
        success_url='/password-change-done/'
    ), name='password_change'),
    
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='libraryapp/password_change_done.html'
    ), name='password_change_done'),
    path('api/add-review/<int:id>/', views.add_review, name='add_review'),
    path('api/delete-review/<int:id>/', views.delete_review, name='delete_review'),
    path("api/edit-review/<int:id>/", views.edit_review, name="edit_review"),
]
