from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

# @ ------------------- Create Routers ↓ -------------------
router.register("books", views.BookViewSet, basename="book")


# @ ------------------- Create Nested Routers ↓ -------------------
# $ Book Nested Routers
book_router = routers.NestedDefaultRouter(router, "books", lookup="book")
book_router.register("comments", views.CommentViewSet, basename="book-comments")


# @ ------------------- Include Routers To URL ↓ -------------------
urlpatterns = router.urls + book_router.urls
