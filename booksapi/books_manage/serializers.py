import logging
from rest_framework import serializers
from .models import Book, ReadingList, ReadingListItem
from authentication.models import User

logger = logging.getLogger(__name__)

class BookSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'genre', 'publication_date', 'description', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def validate(self, data):
        title = data.get('title')
        authors = data.get('authors')
        request = self.context.get('request')

        # Ensure created_by is set to the current user if not provided
        if request and request.user.is_authenticated and not data.get('created_by'):
            data['created_by'] = request.user

        # Check for existing book with same title (title + authors)
        query = Book.objects.filter(title=title)
        if authors:
            query = query.filter(authors=authors)
        
        if self.instance:
            query = query.exclude(id=self.instance.id)

        if query.exists():
            logger.warning(f"Duplicate book creation attempted: title='{title}', authors='{authors}'")
            raise serializers.ValidationError({"title": "A book with this title and authors already exists."})

        logger.debug(f"Validated book data: title='{title}', authors='{authors}'")
        return data

    def create(self, validated_data):
        """
        Log successful book creation.
        """
        book = super().create(validated_data)
        logger.info(f"Book created: title='{book.title}', created_by='{book.created_by.username}'")
        return book


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