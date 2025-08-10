from django.urls import path
from .views import BookListCreateView, BookDetailView, ReadingListListCreateView, ReadingListDetailView, ReadingListItemCreateDeleteView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('reading-lists/', ReadingListListCreateView.as_view(), name='reading-list-list-create'),
    path('reading-lists/<int:pk>/', ReadingListDetailView.as_view(), name='reading-list-detail'),
    path('reading-lists/<int:pk>/items/', ReadingListItemCreateDeleteView.as_view(), name='reading-list-item-create'),
    path('reading-lists/<int:pk>/items/<int:book_id>/', ReadingListItemCreateDeleteView.as_view(), name='reading-list-item-delete'),

]