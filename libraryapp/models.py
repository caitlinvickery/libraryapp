from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    description = models.TextField()
    rating = models.IntegerField(default=0)
    image = models.CharField(max_length=200, default='default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Profile(models.Model):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('user', 'Registered User'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')
    favorite_genre = models.CharField(max_length=100, blank=True) 

    def __str__(self):
        return f"{self.user.username} Profile"

class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.book.title}"

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50)  # like "add_book", "edit_review", etc
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True, blank=True)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="targeted_activities", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.action_type} - {self.timestamp}"