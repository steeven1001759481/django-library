from django.shortcuts import render
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import AuthorSerializer, BookSerializer, BorrowRecordSerializer
from .models import Author, Book, BorrowRecord
# Create your views here.

@api_view(['GET', 'POST'])
def getData(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
def getInd(request, id):
    try:
        author = Author.objects.get(pk=id)  # Fetch the author by ID
    except Author.DoesNotExist:
        return Response({'detail': 'Author not found'})

    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        author.delete()
        return Response({'detail': 'Author deleted successfully'})

@api_view(['GET', 'POST'])
def getBook(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
def getBookDetail(request, id):
    try:
        book = Book.objects.get(pk=id)  # Fetch the book by ID
    except Book.DoesNotExist:
        return Response({'detail': 'Book not found'})

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        book.delete()
        return Response({'detail': 'Book deleted'})


@api_view(['GET','POST'])
def borrowRecord(request):
    if request.method == 'GET':
        records = BorrowRecord.objects.all()
        serializer = BorrowRecordSerializer(records, many=True)
        return Response(serializer.data)
    else:
        book_id = request.data.get('book')
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({'detail': 'Book not found'})
        
        if book.available_copies > 0:
            book.available_copies -= 1
            book.save()

            serializer = BorrowRecordSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)

@api_view(['PUT'])
def returnBook(request, id):
    try:
        borrow_record = BorrowRecord.objects.get(pk=id)
    except BorrowRecord.DoesNotExist:
        return Response({'detail': 'Rented book not found'})

    if borrow_record.return_date:
        return Response({'message': 'Book already returned'})
    
    serializer = BorrowRecordSerializer(borrow_record, data=request.data)

    if serializer.is_valid():
        borrow_record.book.available_copies += 1
        borrow_record.book.save()
        borrow_record.return_date = timezone.now().date()
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

    


