from django.urls import path
from .views import BookListCreateView, BookDetailView, ReadingListListCreateView, ReadingListDetailView, ReadingListItemCreateDeleteView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
   
]