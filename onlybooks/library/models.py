import random
import uuid
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date, timezone


# Genre Table
class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.genre


# Publication Table
class Publication(models.Model):
    publication_id = models.AutoField(primary_key=True)
    publication = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.publication


# Author Table
class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to="library/profile_photos/", null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name


# Book Table
class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    book_img = models.ImageField(upload_to="library/images/", null=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available_copies = models.IntegerField(default=0)
    preview = models.TextField(blank=True)
    publication_date = models.DateField()
    publication = models.ForeignKey(Publication, on_delete=models.SET_NULL, null=True)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.title


# Membership Table


class Membership(models.Model):
    PLAN_CHOICES = [
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
        ('Diamond', 'Diamond'),
    ]

    DURATION_CHOICES = [
        (90, '3 Months'),
        (180, '6 Months'),
        (270, '9 Months'),
        (360, '12 Months'),
    ]

    DEFAULTS = {
        'Gold': {
            'max_books': 5,
            'max_orders_per_month': 10,
            'price_per_3_months': 300,
            'rental_period_days': 30,
        },
        'Platinum': {
            'max_books': 10,
            'max_orders_per_month': 20,
            'price_per_3_months': 600,
            'rental_period_days': 60,
        },
        'Diamond': {
            'max_books': 20,
            'max_orders_per_month': 30,
            'price_per_3_months': 1000,
            'rental_period_days': 90,
        },
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=20, choices=PLAN_CHOICES)
    max_books = models.PositiveIntegerField(editable=False)  # Auto-calculated
    duration_days = models.PositiveIntegerField(choices=DURATION_CHOICES)  # Membership duration in days
    price = models.DecimalField(max_digits=6, decimal_places=2, editable=False)  # Auto-calculated
    rental_period_days = models.PositiveIntegerField(editable=False)  # Auto-calculated
    max_orders_per_month = models.PositiveIntegerField(editable=False)  # Auto-calculated
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(editable=False)  # Auto-calculated

    def save(self, *args, **kwargs):
        # Retrieve defaults for the selected plan
        defaults = self.DEFAULTS.get(self.plan_name, {})

        # Set max_books, max_orders_per_month, rental_period_days, and price dynamically
        self.max_books = defaults.get('max_books', 5)
        self.max_orders_per_month = defaults.get('max_orders_per_month', 10)
        self.rental_period_days = defaults.get('rental_period_days', 30)

        # Calculate price based on the duration
        price_per_3_months = defaults.get('price_per_3_months', 300)
        self.price = (self.duration_days // 90) * price_per_3_months

       # Ensure end_date is calculated
        if not self.end_date:  # Calculate only if not already set
            self.end_date = (self.start_date or date.today()) + timedelta(days=self.duration_days)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} Subscribed to {self.plan_name} Membership"




# Membership Subscription Model (User subscribing to a Membership Plan)





# User Profile
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)
    orders_this_month = models.PositiveIntegerField(default=0)

    def can_place_order(self):
        # Ensure that the user doesn't exceed the order limit for their membership plan
        return self.membership and self.orders_this_month < self.membership.max_orders_per_month

    def __str__(self):
        return self.user.username



# # Payment Model
# class Payment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     payment_date = models.DateTimeField(auto_now_add=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=50, choices=[('Success', 'Success'), ('Failed', 'Failed')],default='Success')

#     def __str__(self):
#         return self.id


# Cart Model
class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username} - {self.book.title} (x{self.quantity})"
    


# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     order_date = models.DateTimeField(auto_now_add=True)
#     payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)
  

#     def calculate_total_price(self):
#         self.total_price = sum(item.price * item.quantity for item in self.order_items.all())
#         self.save()

#     def __str__(self):
#         return f"Order {self.id} by {self.user.username}"


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.quantity} x {self.book.title} in Order {self.order.id}"


#  Order Model
# class Order(models.Model):
#     order_id = models.CharField(max_length=10, unique=True, default=lambda: str(uuid.uuid4().int)[:10], editable=False)
#     book = models.ForeignKey('Book', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     order_date = models.DateTimeField(auto_now_add=True)
#     payment_id=models.ForeignKey(Payment,on_delete=models.CASCADE)
#     def __str__(self):
#         return f"Order {self.order_id} by {self.user.username}"


#  OrderItem Model
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
#     book = models.ForeignKey('Book', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.quantity} x {self.book.title} in Order {self.order.order_id}"


# Rent Model


class Rent(models.Model):
    rent_id = models.CharField(
        max_length=10, 
        primary_key=True, 
        unique=True, 
        editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rental_date = models.DateTimeField()
    return_date = models.DateField()
    payment = models.CharField(max_length=30,editable=False)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)

    

    def generate_rent_id(self):
        while True:
            rent_id = f"RT{random.randint(10000000, 99999999)}"
            if not Rent.objects.filter(rent_id=rent_id).exists():
                return rent_id
            
    def save(self, *args, **kwargs):
        if not self.rent_id:
            # Generate a unique rent ID with the format RTxxxxxxxx
            self.rent_id = self.generate_rent_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} rented {self.book.title}"



class Order(models.Model):
    order_id = models.CharField(
        max_length=10, 
        primary_key=True, 
        unique=True, 
        editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    payment = models.CharField(max_length=30,editable=False)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)

    

    def generate_order_id(self):
        while True:
            order_id = f"OR{random.randint(10000000, 99999999)}"
            if not Order.objects.filter(order_id=order_id).exists():
                return order_id
            
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} ordered {self.book.title}"

