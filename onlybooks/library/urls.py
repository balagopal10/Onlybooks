from django.urls import path
from .views import Index,  author_create, author_delete, author_list, author_update, book_create, book_delete, book_list, book_update, books_by_author, books_by_genre, books_by_publication, browse, change_password, edit_profile, genre_create, genre_delete, genre_list, genre_update, manage_authors, manage_books, manage_genres, manage_publications, membership_list, order_book, order_confirmation, profile_view, publication_create, publication_delete, publication_list, publication_update, rent_book, rent_confirmation,  take_membership,user_login,custom_logout,register, admin_dashboard, user_dashboard
from django.urls import path

urlpatterns=[
    path('',Index,name='home_path'),
    path('useraccount/login/',user_login, name="login"),    
    path('logout/', custom_logout, name="logout"),
    path('useraccount/register/', register, name='register'),
    path('profile/', profile_view, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('change-password/', change_password, name='change_password'),


    path('browse/', browse, name='browse'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/user/', user_dashboard, name='user_dashboard'),
    path('managebooks/',manage_books,name="manage_books"),
    path('manageauthors/',manage_authors,name="manage_authors"),
    path('managegenres/',manage_genres,name="manage_genres"),
    path('manage_publications/',manage_publications,name="manage_pulications"),
    path('books/', book_list, name='book_list'),
    path('books/create/', book_create, name='book_create'),
    path('books/update/<int:pk>/', book_update , name='book_update'),
    path('books/delete/<int:pk>/', book_delete , name='book_delete'),

    path('authors/', author_list, name='author_list'),
    path('authors/create/', author_create, name='author_create'),
    path('authors/update/<int:pk>/', author_update, name='author_update'),
    path('authors/delete/<int:pk>/', author_delete, name='author_delete'),

    path('genres/', genre_list, name='genre_list'),
    path('genres/create/', genre_create, name='genre_create'),
    path('genres/edit/',genre_update,name="genre_update"),
    path('genres/delete/',genre_delete,name="genre_delete"),
    path('publications/', publication_list, name='publication_list'),
    path('publications/create/', publication_create, name='publication_create'),
    path('publications/update/<int:pk>/', publication_update, name='publication_update'),
    path('publications/delete/<int:pk>/', publication_delete, name='publication_delete'),

    

     path('books/author/<int:author_id>/', books_by_author, name='books_by_author'),
    path('genres/<int:genre_id>/books/', books_by_genre, name='books_by_genre'),
   
    path('publications/<int:publication_id>/books/', books_by_publication, name='books_by_publication'),


 path('memberships/', membership_list, name='membership_list'),  
path('takemembership/', take_membership, name='take_membership'),  
path('useraccount/create-rent/<int:book_id>/', rent_book, name='create_rent'),
  path('useraccount/rent-success/<str:rent_id>/', rent_confirmation, name='rent_confirmation'),
  path('useraccount/order/<int:book_id>/', order_book, name='order_book'),
  path('useraccount/order-confirmation/<str:order_id>/', order_confirmation, name='order_confirmation'),
  



]

