from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Author, Book, BookCopy, Member, Loan
from .serializers import BookSerializer, LoanSerializer # Assuming you create basic serializers

# Standard CRUD ViewSets (Easy implementation for managing data)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# --- CUSTOM LOGIC: Borrowing Scenario ---
# Logic based on Sequence Diagram: Member requests -> System Checks -> System Updates

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