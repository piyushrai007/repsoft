from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import Location
from .serializers import LocationSerializer
from django.contrib.auth import authenticate
import requests
from rest_framework.response import Response
from django.conf import settings


# Ensure you set your Google API key in the environment or securely store it

class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'A user with this username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationSearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)
        if not query:
            return Response({"error": "Query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Make a request to Google Maps API
        google_api_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': query,
            'key': settings.GOOGLE_API_KEY
        }
        
        response = requests.get(google_api_url, params=params)
        
        if response.status_code != 200:
            return Response({"error": "Failed to fetch data from Google Maps API"}, status=response.status_code)
        
        data = response.json()
        
        # Extract relevant information from the response
        results = data.get('results', [])
        locations = []
        
        for result in results:
            location = {
                'name': result.get('name'),
                'address': result.get('formatted_address'),
                'latitude': result['geometry']['location']['lat'],
                'longitude': result['geometry']['location']['lng'],
            }
            locations.append(location)
        
        return Response(locations)