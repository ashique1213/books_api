from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import Book, ReadingList, ReadingListItem
from .serializers import BookSerializer, ReadingListSerializer, ReadingListItemSerializer

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            if book.created_by != request.user:
                return Response({"error": "You are not authorized to delete this book."}, status=status.HTTP_403_FORBIDDEN)
            book.delete()
            return Response({"message": "Book deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class ReadingListDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            reading_list = ReadingList.objects.get(pk=pk, user=request.user)
            serializer = ReadingListSerializer(reading_list)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ReadingList.DoesNotExist:
            return Response({"error": "Reading list not found or you do not have permission to access it."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            reading_list = ReadingList.objects.get(pk=pk, user=request.user)
            serializer = ReadingListSerializer(reading_list, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except ReadingList.DoesNotExist:
            return Response({"error": "Reading list not found or you do not have permission to access it."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            reading_list = ReadingList.objects.get(pk=pk, user=request.user)
            reading_list.delete()
            return Response({"message": "Reading list deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except ReadingList.DoesNotExist:
            return Response({"error": "Reading list not found or you do not have permission to access it."}, status=status.HTTP_404_NOT_FOUND)
    

