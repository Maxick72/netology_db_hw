from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class AdvertisementSerializer(serializers.ModelSerializer):


    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at')

    def create(self, validated_data):

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):

        user = self.context["request"].user
        status = data.get("status", getattr(self.instance, "status", None))

        if status == AdvertisementStatusChoices.OPEN:
            open_count = Advertisement.objects.filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN
            ).count()

            if self.instance is None:
                if open_count >= 10:
                    raise serializers.ValidationError(
                        "У вас может быть не более 10 открытых объявлений."
                    )
            else:
                if self.instance.status != AdvertisementStatusChoices.OPEN and open_count >= 10:
                    raise serializers.ValidationError(
                        "У вас может быть не более 10 открытых объявлений."
                    )

        return data
