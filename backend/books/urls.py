from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

# @ Create Routers
router.register("books", views.BookViewSet, basename="book")

# @ Include Routers To URL
urlpatterns = router.urls
