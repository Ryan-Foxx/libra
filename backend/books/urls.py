from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

# @ ------------------- Create Routers ↓ -------------------
router.register("books", views.BookViewSet, basename="book")
router.register("favorites", views.FavoriteViewSet, basename="favorite")


# @ ------------------- Create Nested Routers ↓ -------------------
# $ Book Nested Routers
book_router = routers.NestedDefaultRouter(router, "books", lookup="book")
book_router.register("comments", views.CommentViewSet, basename="book-comments")
book_router.register("images", views.BookImageViewSet, basename="book-images")
book_router.register("ratings", views.RatingViewSet, basename="book-ratings")


# @ ------------------- Include Routers To URL ↓ -------------------
urlpatterns = router.urls + book_router.urls
