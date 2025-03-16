from django.urls import path
from .views import list_libraries, list_users, new_library, get1_library, list_all_books, new_book, books_by_library, get1_book, update_book, delete_book, new_user, get1_user, new_loan, list_loans, loans_by_user, return_book

urlpatterns = [
    path('libraries/', list_libraries, name='list_libraries'),
    path('library/', new_library, name='new_library'),
    path('getLibrary/<int:library_id>/', get1_library, name='get1_library'),
    path('users/', list_users, name='list_users'),
    path('books/', list_all_books, name='list_all_books'),
    path('book/', new_book, name='new_book'),
    path('libraries/<int:library_id>/books/',
         books_by_library, name='books_by_library'),
    path('books/<int:book_id>/', get1_book, name='get1_book'),
    path('updateBook/<int:book_id>/', update_book, name='update_book'),
    path('deleteBook/<int:book_id>/', delete_book, name='delete_book'),
    path('user/', new_user, name='new_user'),
    path('getUser/<int:user_id>/', get1_user, name='get1_user'),
    path('loan/', new_loan, name='new_loan'),
    path('loans/', list_loans, name='list_loans'),
    path('users/<int:user_id>/loans/',
         loans_by_user, name='loans_by_user'),
    path('returnBook/<int:loan_id>/', return_book, name='return_book')
]
