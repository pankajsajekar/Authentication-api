from rest_framework import serializers
from .models import Register

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    mobile = serializers.IntegerField()

    def create(self, validated_data):
        return Register.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.save()
        return instance
    
    def validate_email(self, email):
        lower_email = email.lower()
        if Register.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("EmailID is already Exits")
        return lower_email