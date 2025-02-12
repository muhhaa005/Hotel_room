from rest_framework import serializers
from .models import (
                    UserProfile, City, Hotel, Rooms, RoomImages, Bron, Review,
)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']

class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'country']


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['hotel_name']


class HotelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name', 'hotel_image', 'stars']


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [ 'id', 'city_name', 'image']

class CityDetailSerializer(serializers.ModelSerializer):
    city_hotel = HotelListSerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = ['city_name', 'image', 'city_hotel']


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImages
        fields = ['image']


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ['room_number']


class RoomsListSerializer(serializers.ModelSerializer):
    room_image = ImagesSerializer(many=True, read_only=True)
    room_name = HotelSerializer()
    city = CityListSerializer()

    class Meta:
        model = Rooms
        fields = ['id', 'room_name', 'room_image', 'city', 'price', 'room_type']


class BronSerializer(serializers.ModelSerializer):
    customer = ProfileSerializer()
    hotel = HotelSerializer()
    room = RoomsSerializer()
    class Meta:
        model = Bron
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    hotel_review = HotelSerializer()
    room_review = RoomsSerializer()

    class Meta:
        model = Review
        fields = ['user', 'hotel_review', 'room_review', 'text', 'stars', 'created_date']



class HotelDetailSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer()
    city = CityListSerializer()
    review_hotel = ReviewSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['hotel_name', 'hotel_image', 'owner', 'city', 'description', 'stars',
                  'review_hotel', 'avg_rating', 'count_people']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class RoomsDetailSerializer(serializers.ModelSerializer):
    room_image = ImagesSerializer(many=True, read_only=True)
    room_name = HotelSerializer()
    room_bron = BronSerializer(many=True, read_only=True)
    review_room = ReviewSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()

    class Meta:
        model = Rooms
        fields = ['room_name', 'room_image', 'room_number', 'city', 'description', 'room_type',
                  'status_room', 'room_bron', 'price', 'review_room', 'avg_rating', 'count_people']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()

