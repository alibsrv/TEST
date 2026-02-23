from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Author, Book, BookCopy, Member, Loan
from .serializers import BookSerializer, LoanSerializer 

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


@api_view(['POST'])
def borrow_book(request):
    # 1. Get data 
    member_id = request.data.get('member_id')
    book_copy_id = request.data.get('book_copy_id')

    try:
        member = Member.objects.get(id=member_id)
        copy = BookCopy.objects.get(id=book_copy_id)
    except (Member.DoesNotExist, BookCopy.DoesNotExist):
        return Response({'error': 'Member or Book Copy not found'}, status=404)

    #  Is Book Available? 
    if copy.status != BookCopy.Status.AVAILABLE:
        return Response({'message': 'Book is not available'}, status=status.HTTP_400_BAD_REQUEST)

    #  Create Loan & Set Status 
    loan = Loan.objects.create(member=member, book_copy=copy)
    
    copy.status = BookCopy.Status.LOANED
    copy.save()

    return Response({
        'message': 'You have borrowed the book!',
        'loan_id': loan.id,
        'checkout_date': loan.checkout_date
    }, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # "Mrs. Smith adds a new book"
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            # Check for duplicates is handled by ISBN unique=True in model
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2. Manage a Single Book (Update & Delete)
@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    try:
        # DATA INTEGRITY: Try to get the specific book by Unique ID (pk)
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # "View details of one book"
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # "Mrs. Smith UPDATES price or edition"
        # We pass the existing 'book' instance so DRF knows to Update, not Create
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # "Mrs. Smith DELETES a discontinued book"
        # The 'book' object was already found safely above using the ID
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)