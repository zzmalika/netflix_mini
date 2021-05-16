from django.urls import path

from apps.handbooks import views

urlpatterns = [
    path('category/', views.category_list),
    path('category/<int:pk>/', views.category_detail),
    path('genre/', views.genre_list),
    path('genre/<int:pk>/', views.genre_detail),

    path('country/', views.CountryList.as_view()),
    path('country/<int:pk>/', views.CountryDetail.as_view()),
    path('city/', views.CityList.as_view()),
    path('city/<int:pk>/', views.CityDetail.as_view()),
]
