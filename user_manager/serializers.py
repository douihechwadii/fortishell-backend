from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        is_first_user = User.objects.count() == 0
        user = User(**validated_data)
        user.set_password(password)
        
        if is_first_user:
            user.is_staff = True
            user.is_superuser = True
        
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance