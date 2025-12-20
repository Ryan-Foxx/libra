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
    old_file = old_instance.cover_image
    new_file = instance.cover_image
    if not old_file:
        return
    if not new_file:
        if old_file.path and os.path.exists(old_file.path):
            os.remove(old_file.path)
        return
    if old_file.name != new_file.name:
        if old_file.path and os.path.exists(old_file.path):
            os.remove(old_file.path)


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
