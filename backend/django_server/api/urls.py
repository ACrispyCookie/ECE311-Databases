from django.urls import path
from . import views

urlpatterns = [
    path("departments/", views.department),
    path("departments/<int:departmentCode>/", views.department),
    path("departments/<int:departmentCode>/courses/", views.department_courses),
    path("courses/<int:courseId>/", views.course),
    path("courses/<int:courseId>/categories/", views.course_categories),
    path("categories/<int:courseId>/<str:titleId>/posts/", views.category_posts),
    path("users/<int:userId>/", views.user),
    path("users/<int:userId>/posts/", views.user_posts),
    path("posts/<int:postId>/", views.post),
    path("posts/<int:postId>/reactions/", views.post_reactions),
]