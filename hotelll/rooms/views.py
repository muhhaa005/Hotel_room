from rest_framework.response import  Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import (UserProfile, City, Hotel, Rooms, Bron, Review)
from rest_framework import viewsets, generics, permissions, status
from .serializers import (
                        UserProfileSerializer, CityListSerializer, CityDetailSerializer,  HotelListSerializer, HotelDetailSerializer,
                        RoomsListSerializer, RoomsDetailSerializer, BronSerializer, ReviewSerializer, UserSerializer, LoginSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RoomsFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import CheckBron



class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)





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