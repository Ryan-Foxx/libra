import os

from books.models import Book
from django.db.models.signals import post_delete, post_save, pre_save
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


@receiver(post_save, sender=Book)
def rename_cover_image(sender, instance, created, **kwargs):
    if not instance.cover_image:
        return

    ext = instance.cover_image.name.split(".")[-1]
    new_name = f"books/covers/{instance.id}.{ext}"

    if instance.cover_image.name != new_name:
        instance.cover_image.storage.save(new_name, instance.cover_image.file)
        instance.cover_image.name = new_name
        instance.save(update_fields=["cover_image"])


@receiver(post_delete, sender=Book)
def delete_book_cover_after_book_delete(sender, instance, **kwargs):
    if instance.cover_image:
        try:
            if instance.cover_image.path and os.path.exists(instance.cover_image.path):
                os.remove(instance.cover_image.path)
        except (ValueError, FileNotFoundError):
            pass
