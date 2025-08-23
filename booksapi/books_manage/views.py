import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import Book, ReadingList, ReadingListItem
from .serializers import BookSerializer, ReadingListSerializer, ReadingListItemSerializer

logger = logging.getLogger(__name__)

class BookListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            logger.info(f"Book created by {request.user.username}: {serializer.data.get('title')}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Book creation failed: {serializer.errors}")
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            logger.error(f"Book not found: ID {pk}")
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            if book.created_by != request.user:
                logger.warning(f"Unauthorized delete attempt by {request.user.username} for book ID {pk}")
                return Response({"error": "You are not authorized to delete this book."}, status=status.HTTP_403_FORBIDDEN)
            book.delete()
            logger.info(f"Book deleted by {request.user.username}: ID {pk}")
            return Response({"message": "Book deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            logger.error(f"Book not found for deletion: ID {pk}")
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        
class ReadingListListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reading_lists = ReadingList.objects.filter(user=request.user)
        serializer = ReadingListSerializer(reading_lists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReadingListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            logger.info(f"Reading list created by {request.user.username}: {serializer.data.get('name')}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Reading list creation failed: {serializer.errors}")
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class ReadingListDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            reading_list = ReadingList.objects.get(pk=pk, user=request.user)
            serializer = ReadingListSerializer(reading_list)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ReadingList.DoesNotExist:
            logger.error(f"Reading list not found or unauthorized: ID {pk}")
            return Response({"error": "Reading list not found or you do not have permission to access it."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            reading_list = ReadingList.objects.get(pk=pk, user=request.user)
            serializer = ReadingListSerializer(reading_list, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Reading list updated by {request.user.username}: ID {pk}")
                return Response(serializer.data, status=status.HTTP_200_OK)
            logger.error(f"Reading list update failed: {serializer.errors}")
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except ReadingList.DoesNotExist:
            logger.error(f"Reading list not found or unauthorized: ID {pk}")
            return Response({"error": "Reading list not found or you do not have permission to access it."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            reading_list = ReadingList.objects.get(pk=pk, user=request.user)
            reading_list.delete()
            logger.info(f"Reading list deleted by {request.user.username}: ID {pk}")
            return Response({"message": "Reading list deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except ReadingList.DoesNotExist:
            logger.error(f"Reading list not found or unauthorized: ID {pk}")
            return Response({"error": "Reading list not found or you do not have permission to access it."}, status=status.HTTP_404_NOT_FOUND)
    

class ReadingListItemCreateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            reading_list = ReadingList.objects.get(pk=pk, user=request.user)
            items = ReadingListItem.objects.filter(reading_list=reading_list).order_by('order')
            serializer = ReadingListItemSerializer(items, many=True, context={'request': request})
            logger.info(f"Retrieved items for reading list by {request.user.username}: List ID {pk}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ReadingList.DoesNotExist:
            logger.error(f"Reading list not found or unauthorized: ID {pk}")
            return Response({"error": "Reading list not found or you do not have permission to access it."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        try:
            reading_list = ReadingList.objects.get(pk=pk, user=request.user)
        except ReadingList.DoesNotExist:
            logger.error(f"Reading list not found or unauthorized: ID {pk}")
            return Response({"error": "Reading list not found or you do not have permission to access it."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReadingListItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(reading_list=reading_list)
            logger.info(f"Book added to reading list by {request.user.username}: List ID {pk}, Book ID {serializer.data.get('book')}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Failed to add book to reading list ID {pk}: {serializer.errors}")
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, book_id):
        try:
            reading_list = ReadingList.objects.get(pk=pk, user=request.user)
            item = ReadingListItem.objects.get(reading_list=reading_list, book_id=book_id)
            item.delete()
            logger.info(f"Book removed from reading list by {request.user.username}: List ID {pk}, Book ID {book_id}")
            return Response({"message": "Book removed from reading list successfully."}, status=status.HTTP_204_NO_CONTENT)
        except ReadingList.DoesNotExist:
            logger.error(f"Reading list not found or unauthorized: ID {pk}")
            return Response({"error": "Reading list not found or you do not have permission to access it."}, status=status.HTTP_404_NOT_FOUND)
        except ReadingListItem.DoesNotExist:
            logger.error(f"Book not found in reading list: List ID {pk}, Book ID {book_id}")
            return Response({"error": "Book not found in this reading list."}, status=status.HTTP_404_NOT_FOUND)