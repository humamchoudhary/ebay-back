
from rest_framework import serializers
from base.models import User,Item

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid','username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item 
        fields = ['id', 'name', 'description', 'price', 'image']