# from dj_rest_auth.registration.serializers import RegisterSerializer
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from django_countries.serializers import CountryFieldMixin
# from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError


from .models import UserAddress, Profile

User = get_user_model()


class UserRegistrationSerializer(serializers.Serializer):
   
    """ Serializer for registrating new users using email """
    
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, validated_data):
        password = validated_data['password']
        email = validated_data.get("email", None)

        if not email:
            raise serializers.ValidationError(_("Enter an email."))
        if len(validated_data["password"]) < 8:
            raise ValidationError("Password mustleast 8 charecter.")
        
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")

        # Check if the password contains at least one lowercase letter
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter.")

        # Check if the password contains at least one numeric digit
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one numeric digit.")
        
        if validated_data["password"] != validated_data["confirm_password"]:
            raise serializers.ValidationError(
                _("The two password fields didn't match.")
            )

        return validated_data

    def create(self,  validated_data):
        try:
            user = User.objects.create(
                username=validated_data['username'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email'],
                is_active= True

            )
            user.set_password(validated_data["password"])
            user.save()
            
        except Exception as e:
            if "username" in str(e):
                raise serializers.ValidationError( _(f"username {validated_data['username']} already exists."))
            else:
                raise serializers.ValidationError( _(str(e)))
        return user


# class UserSerializer(serializers.ModelSerializer):

       
class ProfileSerializer(serializers.ModelSerializer):

    """ Serializer class to serialize the user Profile model """

    class Meta:
        model = Profile
        fields = (
            "image",
            "bio",
            "created_at",
            "updated_at",
            "user"
        )
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = instance.user
        representation["username"] =user.username
        representation["first_name"] =user.first_name
        representation["last_name"] =user.last_name
        representation["email"] =user.email
        

        return representation
        


class AddressReadOnlySerializer(CountryFieldMixin, serializers.ModelSerializer):
    """  Address model Serializer class """
    user = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = UserAddress
        fields = "__all__"
        

class UserSerializer(serializers.ModelSerializer):
    """ Serializer class to seralize User model """
    profile = ProfileSerializer(read_only=True)
    addresses = AddressReadOnlySerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            "id", "email", "first_name",  "last_name", "is_active", "profile", "addresses", )


class ShippingAddressSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """ Serializer class to seralize address of type shipping
    For shipping address, automatically set address type to shipping """
    
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserAddress
        fields = "__all__"
        read_only_fields = ("address_type",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["address_type"] = "S"

        return representation


class BillingAddressSerializer(CountryFieldMixin, serializers.ModelSerializer):

    """ Billing address serializer class . For billing address, automatically set address type to billing """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserAddress
        fields = "__all__"
        read_only_fields = ("address_type",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["address_type"] = "B"

        return representation
