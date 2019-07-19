from rest_framework import serializers
from django.contrib.auth import get_user_model
from hotels.models import Hotel, Room, Classification, Reservation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from datetime import datetime, timedelta



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'url', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only':True, 'min_length':8}}


    """ validation when creating new user """
    def create(self, data):
        if not data['email']:
            raise serializers.ValidationError('Email field is essential')
        else:
            user = User.objects.filter(email=data['email'])
            if user:
                raise serializers.ValidationError('This Email is Exist')

        if not data['password']:
            raise serializers.ValidationError('Password field must not be Empty')
        elif len(data['password']) < 8:
            raise serializers.ValidationError('password must be at least 8 characters')
        else:
            data['password'] = make_password(data['password'])

        user = User.objects.create_user(**data)
        return user


    """ validation when updating user """
    def update(self, context, data):
        if not data['username']:
            raise serializers.ValidationError('Username field is essential')
        else:
            user = User.objects.filter(username=data['username']).first()
            if user and not data['username'] == context.username:
                raise serializers.ValidationError('This Username is Taken')

        if not data['email']:
            raise serializers.ValidationError('Email field is essential')
        else:
            user = User.objects.filter(email=data['email']).first()
            if user and not data['email'] == context.email:
                raise serializers.ValidationError('This Email is Exist')

        if not data['password']:
            raise serializers.ValidationError('Password field must not be Empty')
        elif len(data['password']) < 8:
            raise serializers.ValidationError('password must be at least 8 characters')

        context.username = data['username']
        context.email = data['email']
        context.set_password(data['password'])
        context.save()
        return context



class HotelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hotel
        fields = ('id', 'url', 'name', 'stars')



    def create(self, data):
        if not data['stars']:
            raise serializers.ValidationError('every hotel must has a stars number')
        else:
            if data['stars'] > 5 or data['stars'] < 1:
                raise serializers.ValidationError("stars must be in range [1 - 5]")

        if not data['name']:
            raise serializers.ValidationError('Name field is essintial')
        else:
            hotel = Hotel.objects.filter(name=data['name']).first()
            if hotel:
                raise serializers.ValidationError('This Hotel is exist')

        hotel = Hotel.objects.create(**data)
        return hotel


    def update(self, context, data):

        if not data['stars']:
            raise serializers.ValidationError('every hotel must has a stars number')
        else:
            if data['stars'] > 5 or data['stars'] < 1:
                raise serializers.ValidationError("stars must be in range [1 - 5]")
        context.stars = data['stars']
        if not data['name']:
            raise serializers.ValidationError('Name field is essintial')
        else:
            hotel = Hotel.objects.filter(name=data['name']).first()
            if hotel and not context.name == data['name']:
                raise serializers.ValidationError('This Hotel is exist')

        context.name = data['name']
        context.save()
        return context



# class DeletedHotelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Hotel
#         fields = ('id', 'url', 'name', 'stars', 'deleted_at')




class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'url', 'hotel', 'number', 'classification', 'is_avaliable', 'price', 'user')

    def create(self, data):
        if not data['hotel']:
            raise serializers.ValidationError('Container Hotel Must be provided')
        if not data['number']:
            raise serializers.ValidationError('Room Number Must be provided')
        if not data['classification']:
            raise serializers.ValidationError('Roon Classification Must be provided')

        room = Room.objects.filter(hotel=data['hotel'], number=data['number']).first()
        if room:
            raise serializers.ValidationError('this room is already exist')

        """ setting the default price depending on the classification"""
        if not data['price']:
            data['price'] = data['classification'].price

        newroom = Room.objects.create(**data)
        return newroom


    def update(self, context, data):
        if not data['hotel']:
            raise serializers.ValidationError('Container Hotel Must be provided')
        if not data['number']:
            raise serializers.ValidationError('Room Number Must be provided')
        if not data['classification']:
            raise serializers.ValidationError('Roon Classification Must be provided')

        room = Room.objects.filter(hotel=data['hotel'], number=data['number']).first()
        if room and not (context.hotel == data['hotel'] and context.number == data['number']):
            raise serializers.ValidationError('this room is already exist')

        """ setting the default price depending on the classification"""
        if not data['price']:
            data['price'] = data['classification'].price

        context.hotel = data['hotel']
        context.number = data['number']
        context.classification = data['classification']
        context.price = data['price']
        context.is_avaliable = data['is_avaliable']
        context.save()
        return context




class ClassificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Classification
        fields = ("id", "url", "name", "price")

    def create(self, data):
        if not data['name']:
            raise serializers.ValidationError('Classification name must be provided')
        else:
            c = Classification.objects.filter(name=data['name']).first()
            if c:
                raise serializers.ValidationError('this Classification is already exist')

        if not data['price']:
            raise serializers.ValidationError('Price must be provided')
        else:
            if data['price'] <= 0:
                raise serializers.ValidationError('Price value must be Positive number')

        classification = Classification.objects.create(**data)
        return classification


    def update(self, context, data):
        if not data['name']:
            raise serializers.ValidationError('Classification name must be provided')
        else:
            c = Classification.objects.filter(name=data['name']).first()
            if c and not context.name == data['name']:
                raise serializers.ValidationError('this Classification is already exist')

        if not data['price']:
            raise serializers.ValidationError('Price must be provided')
        else:
            if data['price'] <= 0:
                raise serializers.ValidationError('Price value must be Positive number')

        context.name = data['name']
        context.price = data['price']
        return context



class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "url", "user", "room", "paid", "created_at", "started_at", "expired_at")
        extra_kwargs = {'expired_at': {'read_only':True}}

    def update(self, context, data):
        if not data['user']:
            raise serializers.ValidationError('User Field Must be Provided')
        if not data['room']:
            raise serializers.ValidationError('Room Field Must be Provided')
        if not data['paid']:
            raise serializers.ValidationError('Paid Field Must be Provided')
        else:
            if data['paid'] < 0:
                raise serializers.ValidationError('Paid Value must be PPOSITIVE')
            elif data['paid'] < data['room'].price:
                raise serializers.ValidationError('Paid Value must be equal or greater than Room price')
        # if not data['room'].is_avaliable and context.room.is_avaliable:
        #     raise serializers.ValidationError('This Room is not available now')

        context.room = data['room']
        context.user = data['user']
        context.paid = data['paid']
        context.started_at = data['started_at']
        context.expired_at = context.started_at + timedelta(days=1)
        room = context.room
        room.is_avaliable = False
        room.save()
        return context

    def create(self, data):
        if not data['user']:
            raise serializers.ValidationError('User Field Must be Provided')
        if not data['room']:
            raise serializers.ValidationError('Room Field Must be Provided')
        if not data['paid']:
            raise serializers.ValidationError('Paid Field Must be Provided')
        else:
            if data['paid'] < 0:
                raise serializers.ValidationError('Paid Value must be PPOSITIVE')
            elif data['paid'] < data['room'].price:
                raise serializers.ValidationError('Paid Value must be equal or greater than Room price')
        if not data['room'].is_avaliable:
            raise serializers.ValidationError('This Room is not available now')
        r = Reservation.objects.filter(room=data['room'], user=data['user']).first()
        if r:
            raise serializers.ValidationError('this user is already reserving this room')

        data['expired_at'] = data['started_at'] + timedelta(days=1)

        room = data['room']
        room.is_avaliable = False
        room.save()
        reservation = Reservation.objects.create(**data)
        return reservation



    def delete(self, request, pk, format=None):
        r = self.get_object(pk)
        room = r.room
        room.is_avaliable = True
        room.save()
        r.delete()
