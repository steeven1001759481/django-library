from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.getData),
    path('authors/<int:id>', views.getInd),
    path('books/', views.getBook),
    path('books/<int:id>', views.getBookDetail),
    path('borrow/', views.borrowRecord),
    path('borrow/<int:id>/return/', views.returnBook),
]