from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class SuperAdminRegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(write_only=True)
    company_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['fullname', 'company_name', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        fullname = validated_data.pop('fullname')
        company_name = validated_data.pop('company_name')
        password = validated_data.pop('password')

        # Create the super admin user
        user = User.objects.create(
            username=validated_data['email'],  # Set the username to the email
            email=validated_data['email'],
            first_name=fullname,
            company_name=company_name,
            is_superuser=True,  # Give superuser privileges
            is_staff=True,      # Mark as staff to access the admin dashboard
            password=make_password(password)  # Hash the password
        )
        return user




from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fullname', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Create a staff user (not superuser)
        user = User.objects.create_user(
            username=validated_data['email'],  # Using email as username
            email=validated_data['email'],
            password=validated_data['password'],
            is_staff=True,   # Staff user without admin privileges
            is_superuser=False
        )
        user.fullname = validated_data.get('fullname')
        user.save()
        return user


from rest_framework import serializers

class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)


from rest_framework import serializers

class OpenAIRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField(
        required=True,
        help_text="The text prompt for OpenAI to generate a response."
    )
    max_tokens = serializers.IntegerField(
        required=False,
        default=50,
        min_value=1,
        max_value=2048,
        help_text="The maximum number of tokens to generate in the response. Default is 50."
    )
