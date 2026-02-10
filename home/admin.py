from django.contrib import admin
from .models import Author, Book, BookCopy, Member, Loan

# This registers the models so they appear in the Admin Panel
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(Member)
admin.site.register(Loan)