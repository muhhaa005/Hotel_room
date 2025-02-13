from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(17), MaxValueValidator(88)],
                                           null=True, blank=True)
    phone_number = PhoneNumberField()
    STATUS_CHOICES = (
        ('owner', 'owner'),
        ('client', 'client')
    )

    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='client')
    country = models.CharField(max_length=32, default='не указано')

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class City(models.Model):
    city_name = models.CharField(max_length=32, unique=True)
    image = models.ImageField(upload_to='city_photos')

    def __str__(self):
        return self.city_name

class Hotel(models.Model):
    hotel_name = models.CharField(max_length=32)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_hotel')
    description = models.TextField()
    hotel_image = models.ImageField(upload_to='hotel_photos')
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f'{self.hotel_name}, {self.owner}'


    def get_avg_rating(self):
        total = self.review_hotel.all()
        if total.exists():
            return round(sum([i.stars for i in total]) / total.count(), 1)

    def get_count_people(self):
        return self.review_hotel.count()


class Rooms(models.Model):
    room_name = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.PositiveSmallIntegerField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    description = models.TextField()
    TYPE_CHOICES = (
        ('люкс', 'люкс'),
        ('семейный', 'семейный'),
        ('одноместный', 'одноместный'),
        ('двухместный', 'двухместный'),
    )
    room_type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    price = models.PositiveSmallIntegerField()
    STATUS_CHOICES = (
        ('свободен', 'свободен'),
        ('забронирован ', 'забронирован '),
        ('занят', 'занят')
    )
    status_room = models.CharField(max_length=16, choices=STATUS_CHOICES, default='свободен')


    def __str__(self):
        return f'{self.room_name}, {self.status_room}'

    def get_avg_rating(self):
        total = self.review_room.all()
        if total.exists():
            return round(sum([i.stars for i in total]) / total.count(), 1)

    def get_count_people(self):
        return self.review_room.count()


class RoomImages(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, related_name='room_image')
    image = models.ImageField(upload_to='room_photos')


class Bron(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, related_name='room_bron')
    check_in = models.DateField()
    check_out = models.DateField()


    def __str__(self):
        return f'{self.customer}'


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel_review = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='review_hotel')
    room_review = models.ForeignKey(Rooms, on_delete=models.CASCADE, related_name='review_room')
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'stars')

    def __str__(self):
        return f'{self.user}, {self.stars}'