from django.db import models
import uuid

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    genre = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title

class BookCopy(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        LOANED = 'LOANED', 'Loaned'
        MAINTENANCE = 'MAINTENANCE', 'Maintenance'

    class Condition(models.TextChoices):
        NEW = 'NEW', 'New'
        GOOD = 'GOOD', 'Good'
        WORN = 'WORN', 'Worn'

    inventory_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    shelf_location = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.GOOD)
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies')

    def __str__(self):
        return f"{self.book.title} ({self.inventory_id})"

class Member(models.Model):
    user_id = models.IntegerField(unique=True) 
    email = models.EmailField()
    membership_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email

class Loan(models.Model):
    checkout_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='loans')
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, related_name='loans')

    def __str__(self):
        return f"Loan: {self.book_copy.book.title} by {self.member.email}"
