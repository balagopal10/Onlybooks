from django import forms
from .models import  User, Book, Author, Genre,Publication, Membership, Rent
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




class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['plan_name', 'duration_days']
        labels = {
            'plan_name': 'Membership Plan',
            'duration_days': 'Duration (in months)',
        }
        widgets = {
            'plan_name': forms.Select(attrs={'class': 'form-control'}),
            'duration_days': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        plan_name = cleaned_data.get('plan_name')
        duration_days = cleaned_data.get('duration_days')

        # Additional validations if needed
        if not plan_name:
            self.add_error('plan_name', 'Please select a membership plan.')
        if not duration_days:
            self.add_error('duration_days', 'Please select a valid duration.')

        return cleaned_data





class UpgradeSubscriptionForm(forms.Form):
    plan = forms.ChoiceField(choices=[
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
        ('Diamond', 'Diamond')
    ])

class RentForm(forms.Form):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
    ]
    payment_mode = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)

class OrderForm(forms.Form):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
    ]
    payment_mode = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)
