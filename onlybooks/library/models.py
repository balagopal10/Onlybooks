from django.db import models
from django.contrib.auth.models import User


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
    profile_photo=models.ImageField(upload_to="library/profile_photos/", null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

# Book Table
class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    book_img=models.ImageField(upload_to="library/images/", null=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    availability_status = models.BooleanField(default=True)  # True = Available, False = Unavailable
    preview = models.TextField(blank=True)
    publication_date = models.DateField()
    publication = models.ForeignKey(Publication, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title



# Subscription Table
class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=50, choices=[
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
        ('Diamond', 'Diamond')
    ])
    start_date = models.DateField()
    end_date = models.DateField()
    max_rentals = models.PositiveIntegerField(default=2)  # E.g., Gold=2, Platinum=5, Diamond=10

    def save(self, *args, **kwargs):
        # Set plan-specific max_rentals
        if self.plan == 'Gold':
            self.max_rentals = 2
        elif self.plan == 'Platinum':
            self.max_rentals = 5
        elif self.plan == 'Diamond':
            self.max_rentals = 10
        super().save(*args, **kwargs)


# Rental Table
class Rental(models.Model):
    rental_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rental_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, default='Borrowed')  # Borrowed, Returned, Overdue

# Notification Table
class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rental = models.ForeignKey(Rental, on_delete=models.SET_NULL, null=True, blank=True)
    due = models.ForeignKey('Due', on_delete=models.SET_NULL, null=True, blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()

# Order Table
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# Payment Table
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_mode = models.CharField(max_length=20, choices=[
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Net Banking', 'Net Banking'),
        ('Cash', 'Cash')
    ])

# Due Table
class Due(models.Model):
    due_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, default='Unpaid')  # Paid or Unpaid
    due_date = models.DateField()

# Review Table
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Ratings 1 to 5
    comment = models.TextField()
    review_date = models.DateField(auto_now_add=True)
