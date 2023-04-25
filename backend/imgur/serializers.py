import datetime

import PIL
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *
from .validators import *
from allauth.account.models import EmailAddress

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        if user.is_superuser:
            token["is_superuser"] = True
        else:
            token["is_superuser"] = False

        return token


# ImgurUserSerializer
class ImgurUserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImgurUser
        fields = "__all__"

    # error_messages = {
    #     "required": "To pole jest wymagane.",
    #     "blank": "To pole nie może być puste.",
    #     "invalid": "Niepoprawny adres email.",
    # }

    username = serializers.CharField(
        validators=[validate_username],
        # error_messages=error_messages,
        required=False,
    )

    email = serializers.EmailField(
        validators=[validate_email],
        # error_messages=error_messages,
        required=False,
    )

    password = serializers.CharField(
        validators=[validate_password],
        # error_messages=error_messages,
        write_only=True,
        required=False,
    )

    phone_number = serializers.CharField(
        validators=[validate_phone_number],
        # error_messages=error_messages,
        required=False,
    )

    first_name = serializers.CharField(
        validators=[validate_first_name],
        # error_messages=error_messages,
        required=False,
    )

    last_name = serializers.CharField(
        validators=[validate_last_name],
        # error_messages=error_messages,
        required=False,
    )

    def create(self, validated_data):
        imgur_user = ImgurUser.objects.create(
            email=validated_data.get("email"),
            username=validated_data.get("email"),
            phone_number=validated_data.get("phone_number"),
            is_active=False,  # True - dostep do logowania, False - brak dostepu
        )
        # set_password haszuje haslo
        imgur_user.set_password(validated_data.get("password"))
        imgur_user.save()
        email_address = EmailAddress.objects.create(user=imgur_user, email=validated_data['email'], primary=True, verified=False)
        return imgur_user

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        password = validated_data.get("password")
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class ImgurUserCreateSerializer(ImgurUserBaseSerializer):
    class Meta:
        model = ImgurUser
        fields = "__all__"

    email = serializers.EmailField(
        validators=[validate_email],
        # error_messages=ImgurUserBaseSerializer.error_messages,
        required=True,
    )

    password = serializers.CharField(
        validators=[validate_password],
        # error_messages=ImgurUserBaseSerializer.error_messages,
        write_only=True,
        required=True,
    )


# ImageSerializer
class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        validators=[
            validate_image,
            validate_image_name,
        ]
    )

    class Meta:
        model = Image
        fields = "__all__"

    def create(self, validated_data):
        image = validated_data.get("image")
        pil_image = PIL.Image.open(image)

        new_image = Image.objects.create(
            name=image.name,
            size=pil_image.size,
            mime_type=pil_image.format,
            image=image,
            # post=validated_data.get('post')
        )
        new_image.path = new_image.image.path
        new_image.save()

        return new_image

    def update(self, instance, validated_data):
        image = validated_data.get("image")
        pill_image = PIL.Image.open(image)

        instance.name = image.name
        instance.size = pill_image.size
        instance.mime_type = pill_image.format
        instance.image = image
        instance.path = instance.image.path
        instance.save()

        return instance


class PostSerializer(serializers.ModelSerializer):
    # image = ImageSerializer(required=True)
    record_id = serializers.IntegerField(required=False)
    class Meta:
        model = Post
        # exclude = ["expirationDate"]
        fields = "__all__"

    def create(self, validated_data):
        expiration_date = datetime.datetime.now() + datetime.timedelta(days=30)
        validated_data["expirationDate"] = expiration_date
        post = Post.objects.create(
            imgur_user=validated_data.get("imgur_user"),
            title=validated_data.get("title"),
            description=validated_data.get("description"),
            tag=validated_data.get("tag"),
            expirationDate=validated_data.get("expirationDate"),
            record_id=0,
        )
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.tag = validated_data.get("tag", instance.tag)

        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class SubcommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcomment
        fields = "__all__"


class ReactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = "__all__"
