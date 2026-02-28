from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')

        user = get_user_model().objects.create_user(
            password=password,
            **validated_data
        )

        Token.objects.create(user=user)
        return user



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'bio', 'followers','profile_picture')


User = get_user_model()

class FollowSerializer(serializers.ModelSerializer):
    target_user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ('target_user_id',)

    def validate_target_user_id(self, value):
        user = self.context['request'].user
        if user.id == value:
            raise serializers.ValidationError("You cannot follow/unfollow yourself.")
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist.")
        return value
