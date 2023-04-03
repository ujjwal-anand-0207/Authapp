from rest_framework  import serializers
from account.models import User
from xml.dom import ValidationErr
from django.utils.encoding import smart_str ,force_bytes ,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
    # For confirming password field during registration process
    password2 =serializers.CharField(style ={'input_type':'password'},
                                         write_only=True)
    class Meta:
        model = User
        
        fields =['email','name', 'password', 'password2','tc']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    #validating Password and confirm password
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password doesn't match")
        return attrs
    
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields =['id','email','name']

class UserChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},
                                   write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},
                                   write_only=True)
    class Meta:
        model =User
        fields =['password','password2']
        
    def validate(self,attrs):
        psw= attrs.get("password")
        psw2=attrs.get("password2")
        user = self.context.get('user')
        if psw != psw2:
            raise serializers.ValidationError("Password doesn't match")
        user.set_password(psw)
        user.save()
        return attrs
    
class SendPasswordResetSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:        
        fields=['email']

    def validate(self,attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link ='http://localhost:3000/api/user/reset/'+uid+'/'+token
            print(link)
            #send email
            data ={
                'subject': 'RESET PASSWORD',
                'body':link+" reset link",
                'to_email':user.email

            }
            Util.send_email(data)
            return attrs
        else:
            raise ValidationErr('Not register user')
        

class UserPasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},
                                   write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},
                                   write_only=True)
    class Meta:
        model =User
        fields =['password','password2']
        
    def validate(self,attrs):
        try:
            psw= attrs.get("password")
            psw2=attrs.get("password2")
            uid = self.context.get('uid')
            token = self.context.get('token')
            if psw != psw2:
                raise serializers.ValidationError("Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationErr('token doesnt match or token expired')
            user.set_password(psw)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationErr('token doesnt match or token expired')
            