from django.contrib import admin
from .models import  Genre, Membership, Order, Publication, Author, Book,  Rent, UserProfile, Cart

# Register your models here.
admin.site.register(Genre)
admin.site.register(Publication)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Membership)
admin.site.register(Order)
admin.site.register(UserProfile)

admin.site.register(Cart)

admin.site.register(Rent)

