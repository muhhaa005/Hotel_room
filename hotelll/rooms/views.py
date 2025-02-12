from .models import (UserProfile, City, Hotel, Rooms, Bron, Review)
from rest_framework import viewsets, generics, permissions
from .serializers import (
                        UserProfileSerializer, CityListSerializer, CityDetailSerializer,  HotelListSerializer, HotelDetailSerializer,
                        RoomsListSerializer, RoomsDetailSerializer, BronSerializer, ReviewSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RoomsFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import CheckBron



class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class UserProfileEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class CityListAPIView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CityListSerializer

class CityDetailAPIView(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CityDetailSerializer


class HotelListAPIView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['hotel_name']

class HotelDetailAPIView(generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelDetailSerializer


class RoomsListAPIView(generics.ListAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomsListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckBron]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RoomsFilter
    search_fields = ['hotel_name']
    ordering_fields = ['price']


class RoomsDetailAPIView(generics.RetrieveAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomsDetailSerializer


class BronListAPIView(generics.ListCreateAPIView):
    queryset = Bron.objects.all()
    serializer_class = BronSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckBron]



class ReviewCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(id=self.request.user.id)