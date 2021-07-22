from django.db import models


class MarketPlaceItem(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField(null=True, blank=True)
    price_is_visible = models.BooleanField(default=True)

    guid = models.UUIDField(auto_created=True, primary_key=True, unique=True)

    asset = models.ForeignKey('Asset', null=True, related_name='parent', on_delete=models.CASCADE)
    series = models.ForeignKey('Series', null=True, related_name='parent', on_delete=models.CASCADE)


class Asset(models.Model):
    quantity = models.PositiveIntegerField()
    royalties = models.PositiveIntegerField()
    content_url = models.TextField()
    series = models.ForeignKey(MarketPlaceItem, related_name='assets', on_delete=models.CASCADE)


class Series(models.Model):

    visibility = models.CharField(max_length=30)