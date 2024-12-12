from django import forms
from .models import User, Book, Author, Genre,Publication, Subscription, Rental
from django.forms import ValidationError

class MyLoginForm(forms.Form): #using Form
    username= forms.CharField(
        min_length=3,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'})
        )
    password= forms.CharField(
        widget= forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'})
        )

#for registration or signup
class UserRegistrationForm(forms.ModelForm): #using ModelForm
    #password
    password= forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    #for confirm password
    password2= forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
    )

    #since inheritance from ModelForm, I can use the model to declare the fields
    class Meta:
        model= User
        #fields in the built in Model User
        fields= ('username','first_name','email','password')

        #overriding a inbuilt method to check the password input = confirm password
        #clean_<fieldname>
        def clean_password2(self):
            cd= self.cleaned_data
            if cd['password'] != cd['password2']:
                raise ValidationError('Password does not match!!!')
            
            return cd['password2']
        
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']



class AddBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'book_img', 'author', 'genre', 'price', 'publication_date', 'available_copies', 'preview', 'publication']
        widgets = {
            'publication_date': forms.DateInput(attrs={
                'type': 'date',  # HTML5 date input
                'class': 'form-control',  # Add Bootstrap class for styling (optional)
                'placeholder': 'Select a date'  # Placeholder text (optional)
            }),
        }

    #validation for book_title
    def clean_book_title(self):
        book_title= self.cleaned_data.get('title')
        if not book_title:
            raise ValidationError('This field is required')
        if len(book_title)<5:
            raise ValidationError('Title should be atleast 5 characters long')
        return book_title

    #validation for book_image
    def clean_book_image(self):
        book_image= self.cleaned_data.get('book_img')
        if book_image:
            extensions=['png','jpg','jpeg','avif','webp']
            image_extension= book_image.name.lower().split('.')[-1]
            if image_extension not in extensions:
                raise ValidationError('Image must be in PNG, JPG, JPEG, AVIF, WEBP format!')
        return book_image
    
class EditBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','book_img','author', 'genre','price', 'publication_date', 'available_copies', 'preview','publication']
        widgets = {
            'publication_date': forms.DateInput(attrs={
                'type': 'date',  # HTML5 date input
                'class': 'form-control',  # Add Bootstrap class for styling (optional)
                'placeholder': 'Select a date'  # Placeholder text (optional)
            }),
        }

class AddAuthor(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name','profile_photo', 'description']
       

    

class AddGenre(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['genre']


class AddPublication(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['publication']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['plan', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class UpgradeSubscriptionForm(forms.Form):
    plan = forms.ChoiceField(choices=[
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
        ('Diamond', 'Diamond')
    ])




class RentBookForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['book', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
