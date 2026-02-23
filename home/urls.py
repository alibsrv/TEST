from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, borrow_book
from . import views

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('borrow/', borrow_book, name='borrow-book'), 
    path('books/', views.book_list, name='book-list'),
    path('books/<int:pk>/', views.book_detail, name='book-detail'),
]