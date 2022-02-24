from django.urls import path
from categories import views

urlpatterns = [
    path('listCategory',views.CategoryListView.as_view(),name="listCategory"),
    path('createCategory',views.CategoryCreateView.as_view(),name="createCategory"),
    path('updateCategory/<int:pk>',views.CategoryUpdateView.as_view(),name="updateCategory"),
    path('deleteCategory/<int:pk>',views.CategoryDeleteView.as_view(),name="deleteCategory"),
]
