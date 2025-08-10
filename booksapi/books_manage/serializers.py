from rest_framework import serializers
from .models import Book, ReadingList, ReadingListItem
from authentication.models import User

class BookSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'genre', 'publication_date', 'description', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class ReadingListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ReadingList
        fields = ['id', 'user', 'name', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']


class ReadingListItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book', write_only=True)

    class Meta:
        model = ReadingListItem
        fields = ['id', 'reading_list', 'book', 'book_id', 'order', 'added_at']
        read_only_fields = ['reading_list', 'book', 'added_at']