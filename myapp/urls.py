from django.urls import path
from .views import SignupView, LoginView, LocationListCreateView, LocationSearchView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('locations/', LocationListCreateView.as_view(), name='location-list-create'),
    path('locations/search/', LocationSearchView.as_view(), name='location-search'),
]
