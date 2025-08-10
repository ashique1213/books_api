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