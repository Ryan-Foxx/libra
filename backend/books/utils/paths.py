def book_cover_upload_path(instance, filename):
    return f"books/covers/temp_{filename}"


def book_image_upload_path(instance, filename):
    return f"books/images/temp_{filename}"
