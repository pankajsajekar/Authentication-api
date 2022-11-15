from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util

# third part-library
from phonenumber_field.serializerfields import PhoneNumberField

# class RegisterSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=200)
#     email = serializers.CharField(max_length=200)
#     password = serializers.CharField(max_length=200)
#     mobile = serializers.IntegerField()

#     def create(self, validated_data):
#         return Register.objects.create(**validated_data)
        
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.email = validated_data.get('email', instance.email)
#         instance.password = validated_data.get('password', instance.password)
#         instance.mobile = validated_data.get('mobile', instance.mobile)
#         instance.save()
#         return instance
    
#     def validate_email(self, email):
#         lower_email = email.lower()
#         if Register.objects.filter(email__iexact=lower_email).exists():
#             raise serializers.ValidationError("EmailID is already Exits")
#         return lower_email


class UserRegistrationSerializer(serializers.ModelSerializer):
    mobile = PhoneNumberField()
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    is_candidate = serializers.BooleanField(default=False)
    is_employer = serializers.BooleanField(default=False)
    class Meta:
        model = User
        fields = ['email','name','mobile', 'password', 'password2', 'is_candidate', 'is_employer']
        extra_kwargs = {'password':{'write_only': True}}
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password does not match.')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerialiser(serializers.ModelSerializer):
    email = serializers.EmailField()
    user_type = serializers.BooleanField(default=False)
    class Meta:
        model = User
        fields = ['email', 'password','user_type']
        
    def validate(self, attrs):
        user_type = attrs.get('user_type')
        if user_type == True:
            print("user type value get")
        else:
            raise serializers.ValidationError('login Cridential not match with user.')
        return attrs



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'mobile']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password does not match.')
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print(uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print(token)
            link = 'http://127.0.0.1:8000/api/user/reset-password/'+uid+'/' + token+ '/'
            print(link)
            # send email
            body = 'Click following link to reset your password ' + link
            data = {
                'subject': 'Reset your password',
                'body':body,
                'to_email': user.email
            }
            # Util.send_email(data)
            return attrs
        else:
            raise ValueError("Your are not a Registered User")

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError('Password and Confirm Password does not match.')
            id = smart_str(urlsafe_base64_decode(uid))  
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return ValueError('Token is not Valid or expired.')
            user.set_password(password)
            user.save() 
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValueError('Token is not Valid or expired.')

class AdminLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password', 'is_admin']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['email', 'mobile', 'name', 'register_id']
        fields = '__all__'

class UserLogoutSerializer(serializers.Serializer):
    # refresh = serializers.CharField(max_length=255)

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    # def validate(self, attrs):
    #     self.token = attrs['access']
    #     return attrs

    # def save(self, **kwargs):
    #     try:
    #         RefreshToken(self.token).blacklist()

    #     except:
    #        ValueError('bad_token')
