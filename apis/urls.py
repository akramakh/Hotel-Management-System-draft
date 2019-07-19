from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from. import viewsets
from rest_framework import routers

router = routers.DefaultRouter()

router.register('users', viewsets.UserViewSet)
router.register('hotels', viewsets.HotelViewSet, basename="hotel")
router.register('rooms', viewsets.RoomViewSet, basename="room")
router.register('available-rooms-only', viewsets.AvailableRoomViewSet,basename='available-room')
router.register('classifications', viewsets.ClassificationViewSet, basename="classification")
router.register('reservations', viewsets.ReservationViewSet, basename="reservation")

# router.register('deleted-users', viewsets.DeletedUserViewSet)
router.register('deleted-hotels', viewsets.DeletedHotelViewSet, basename='deleted-hotel')
router.register('deleted-rooms', viewsets.DeletedRoomViewSet, basename='deleted-room')
router.register('deleted-classifications', viewsets.DeletedClassificationViewSet, basename='deleted-classification')
router.register('deleted-reservations', viewsets.DeletedReservationViewSet, basename='deleted-reservation')

urlpatterns = [
    path('',include(router.urls)),
    # path('delete-res/', viewsets.delete_res, ),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
