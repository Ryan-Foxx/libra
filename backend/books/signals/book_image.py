import os

from books.models import BookImage
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=BookImage)
def delete_old_book_image(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_instance = BookImage.objects.get(pk=instance.pk)
    except BookImage.DoesNotExist:
        return
    if old_instance.image and old_instance.image != instance.image:
        old_path = old_instance.image.path
        if os.path.exists(old_path):
            os.remove(old_path)
