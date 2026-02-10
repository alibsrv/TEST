from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, borrow_book

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('borrow/', borrow_book, name='borrow-book'), 
]