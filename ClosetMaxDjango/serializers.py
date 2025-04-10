from rest_framework import serializers
from .models import Clothes, CustomUser


# User Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # Make sure the password is only written and not exposed in the response
        }

    def create(self, validated_data):
        # Automatically hashes the password with set_password
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data.get('phone', None),  # Phone is optional
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


from .models import Clothes, CustomUser, Closet

class ClosetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Closet
        fields = ['id', 'name', 'description', 'created_at']


class ClothesSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='user')
    closet_id = serializers.PrimaryKeyRelatedField(queryset=Closet.objects.all(), source='closet', allow_null=True, required=False)

    class Meta:
        model = Clothes
        fields = ['id', 'user_id', 'closet_id', 'material', 'size', 'brand', 'season', 'clothing_type', 'favorite', 'image', 'color']
        extra_kwargs = {
            'material': {'required': False, 'allow_null': True},
            'brand': {'required': False, 'allow_null': True},
            'clothing_type': {'required': False, 'allow_null': True},
            'favorite': {'required': False, 'allow_null': True},
            'image': {'required': True},
        }

