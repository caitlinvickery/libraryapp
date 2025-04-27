from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    favorite_genre = forms.ChoiceField(choices=[
    ('fiction', 'Fiction'),
    ('nonfiction', 'Nonfiction'),
    ('scifi', 'Sci-Fi'),
    ('fantasy', 'Fantasy'),
    ('romance', 'Romance'),
])
    username = forms.CharField(max_length=150, help_text='')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash password
        if commit:
            user.save()
            # Create the profile manually since we're capturing extra data
            Profile.objects.create(
                user=user,
                favorite_genre=self.cleaned_data['favorite_genre']
            )
        return user
    
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    favorite_genre = forms.ChoiceField(choices=[
        ('fiction', 'Fiction'),
        ('nonfiction', 'Nonfiction'),
        ('scifi', 'Sci-Fi'),
        ('fantasy', 'Fantasy'),
        ('romance', 'Romance'),
    ])

    class Meta:
        model = Profile
        fields = ['favorite_genre']  # Profile-only field

    def save(self, user, commit=True):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = super().save(commit=False)
            profile.user = user
            profile.save()
        return user
