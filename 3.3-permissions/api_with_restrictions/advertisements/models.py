from django.conf import settings
from django.db imporfrom django.db import models
from django.conf import settings

class AdvertisementStatus(models.TextChoices):
    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"

class Advertisement(models.Model):
    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(choices=AdvertisementStatus.choices, default=AdvertisementStatus.OPEN)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def favorites(self, request):
        favorites = Advertisement.objects.filter(favorite__user=request.user)
        page = self.paginate_queryset(favorites)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(favorites, many=True)
        return Response(serializer.data)