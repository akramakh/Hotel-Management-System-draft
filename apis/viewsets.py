from rest_framework import viewsets, permissions, authentication
from rest_framework.response import Response
from rest_framework import status
# from rest_framework import mixins
from rest_framework import generics
from .serializers import UserSerializer, HotelSerializer, RoomSerializer, ClassificationSerializer, ReservationSerializer
from django.contrib.auth import get_user_model
from hotels.models import Hotel, Room, Classification, Reservation



class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

#######################################################3


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class DeletedHotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.deleted_only()
    serializer_class = HotelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


#######################################################


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class AvailableRoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.filter(is_avaliable=True).all()
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class DeletedRoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.deleted_only()
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)



#######################################################3


class ClassificationViewSet(viewsets.ModelViewSet):
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer
    permission_classes = (permissions.IsAdminUser,)


class DeletedClassificationViewSet(viewsets.ModelViewSet):
    queryset = Classification.objects.deleted_only()
    serializer_class = ClassificationSerializer
    permission_classes = (permissions.IsAdminUser,)


#######################################################3


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    """ making room availablr for future reservations"""
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        room = obj.room
        room.is_avaliable = True
        room.save()
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeletedReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.deleted_only()
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)