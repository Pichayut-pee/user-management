from django.db import models


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.TextField(max_length=512, unique=True)
    password = models.TextField(max_length=512)
    salt = models.TextField(max_length=512, default="")
    line_user_id = models.TextField(max_length=512, default="")
    role = models.TextField(max_length=100)
    tier = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "line_user_id": self.line_user_id,
            "role": self.role,
            "tier": self.tier,
        }


class UsersProfile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    email = models.TextField(max_length=512, unique=True)
    name = models.TextField(max_length=512)


class UsersFavoriteSearch(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    price_search_from = models.IntegerField(default=0)
    price_search_to = models.IntegerField(default=100000000)
    space_search_from = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    space_search_to = models.DecimalField(max_digits=5, decimal_places=2,  default=999)
    room_search_from = models.IntegerField(default=0)
    room_search_to = models.IntegerField(default=99)
    toilet_search_from = models.IntegerField(default=0)
    toilet_search_to = models.IntegerField(default=99)
    floor_search_from = models.IntegerField(default=0)
    floor_search_to = models.IntegerField(default=0)
    location_search = models.CharField(max_length=1000 ,blank=True, null=True)
    desc_search = models.CharField(max_length=1000 ,blank=True, null=True)
    limit = models.IntegerField(default=5)

    def serialize(self):
        return {
            "price_search_from": self.price_search_from,
            "price_search_to": self.price_search_to,
            "space_search_from": self.space_search_from,
            "space_search_to": self.space_search_to,
            "room_search_from": self.room_search_from,
            "room_search_to": self.room_search_to,
            "toilet_search_from": self.toilet_search_from,
            "toilet_search_to": self.toilet_search_to,
            "floor_search_from": self.floor_search_from,
            "floor_search_to": self.floor_search_to,
            "location_search": self.location_search,
            "desc_search": self.desc_search,
            "limit": self.limit
        }
