from django.contrib import admin
from .models import  Genre, Membership, Publication, Author, Book,  Order, Payment, Rent, UserProfile, Cart, OrderItem

# Register your models here.
admin.site.register(Genre)
admin.site.register(Publication)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Membership)

admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(Rent)

