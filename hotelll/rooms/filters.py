from django_filters import FilterSet
from .models import Rooms, Hotel


class RoomsFilter(FilterSet):
    class Meta:
        model = Rooms
        fields = {
            'city': ['exact'],
            'room_type': ['exact'],
            'price': ['gt', 'lt'],
            'status_room': ['exact'],
        }


