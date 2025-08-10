from django.db import models
from authentication.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    publication_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books'

class ReadingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_lists')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reading_lists'
        unique_together = ('user', 'name')


class ReadingListItem(models.Model):
    reading_list = models.ForeignKey(ReadingList, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_list_items')
    order = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reading_list_items'
        unique_together = ('reading_list', 'book')
        ordering = ['order']
