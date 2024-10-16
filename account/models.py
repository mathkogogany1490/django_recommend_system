from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_id = models.IntegerField(null=True)
    profile_image = models.ImageField("프로필 이미지", upload_to="account/profile",
                                      blank=True)
    short_description = models.TextField('소개글', blank=True)
    def __str__(self):
        return self.username  # 사용자 이름을 기본 출력으로 설정


