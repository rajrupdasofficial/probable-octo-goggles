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