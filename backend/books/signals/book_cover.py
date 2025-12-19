import os

from books.models import Book
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Book)
def delete_old_cover(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_instance = Book.objects.get(pk=instance.pk)
    except Book.DoesNotExist:
        return
    if old_instance.cover_image and old_instance.cover_image != instance.cover_image:
        old_path = old_instance.cover_image.path
        if os.path.exists(old_path):
            os.remove(old_path)
