import os

from books.models import BookImage
from django.db.models.signals import post_delete, post_save, pre_save
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


@receiver(post_save, sender=BookImage)
def rename_book_image(sender, instance, created, **kwargs):
    if not instance.image:
        return
    ext = instance.image.name.split(".")[-1]
    new_name = f"books/images/{instance.book.id}_{instance.id}.{ext}"
    if instance.image.name != new_name:
        instance.image.storage.save(new_name, instance.image.file)
        instance.image.name = new_name
        instance.save(update_fields=["image"])


@receiver(post_delete, sender=BookImage)
def delete_image_file_after_image_object_delete(sender, instance, **kwargs):
    if instance.image:
        if instance.image.path and os.path.exists(instance.image.path):
            os.remove(instance.image.path)
