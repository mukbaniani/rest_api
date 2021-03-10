from rest_framework import serializers
from .models import Post, Category, Comment
from django.contrib.auth.models import User


class PostSerializers(serializers.ModelSerializer):
    class Meta: 
        model = Post
        fields = '__all__'
        read_only_fields = ['user']


class CategorySerializer(serializers.ModelSerializer):

    post_sum = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user']


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        account = User(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
        )
        password = self.validated_data.get('password')
        password2 = self.validated_data.get('password2')
        print(password2)
        if password != password2:
            raise serializers.ValidationError('პაროლი არ ემთხვევა ერთმანეთს')
        account.set_password(password)
        account.save()
        return account