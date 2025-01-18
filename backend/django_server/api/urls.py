from django.urls import path
from . import views

urlpatterns = [
    path("department/", views.department),
    path("department/courses/", views.department_courses),
    path("courses/<str:courseId>/", views.course),
    path("courses/<str:courseId>/categories/", views.course_categories),
    path("categories/<str:courseId>/<str:titleId>/posts/", views.category_posts),
    path("users/<str:userId>/", views.user),
    path("users/<str:userId>/posts/", views.user_posts),
    path("posts/<int:postId>/", views.post),
    path("posts/", views.post),
    path("posts/<int:postId>/reactions/", views.post_reactions),
]