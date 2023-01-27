from rest_framework import serializers
from account.models import User
from django.contrib.auth.hashers import make_password
class UserRSerializer(serializers.HyperlinkedModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email','name','password','password2','tc']
        extra_kwargs = {'password':{'write_only':True}}
        def create(self, validated_data):
            return super(UserRSerializer, self).create(validated_data)

class UserLSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields =['id','email','name']

class PasChSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password!=password2:
            raise serializers.ValidationError('Passwords wont match')
        user.make_password(password)
        user.save()
        return attrs