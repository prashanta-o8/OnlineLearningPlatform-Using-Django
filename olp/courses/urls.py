from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('create_course/', views.create_course, name='create_course'),
    path('create_lesson/<int:course_id>/', views.create_lesson, name='create_lesson'),
    path('progress/', views.student_progress, name='student_progress'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
]