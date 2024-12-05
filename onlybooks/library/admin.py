from django.contrib import admin
from .models import Genre, Publication, Author, Book, Subscription, Rental, Notification, Order, Payment, Due, Review

# Register your models here.
admin.site.register(Genre)
admin.site.register(Publication)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Subscription)
admin.site.register(Rental)
admin.site.register(Notification)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Due)
admin.site.register(Review)
