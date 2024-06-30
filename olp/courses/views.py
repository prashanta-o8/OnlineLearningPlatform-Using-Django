from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Enrollment, Progress
from django.contrib import messages
from .forms import CourseForm, LessonForm

# Create your views here.
def home(request):
    courses = Course.objects.all()
    return render(request, 'courses/home.html', {'courses': courses})

@login_required
def course_list(request):
    if request.user.is_staff:
        courses = Course.objects.filter(instructor=request.user)
    else:
        courses = Course.objects.filter(enrollments__student=request.user)
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists() if request.user.is_authenticated else False
    context = {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.user.is_staff or Enrollment.objects.filter(student=request.user, course=lesson.course).exists():
        return render(request, 'courses/lesson_detail.html', {'lesson': lesson})
    else:
        messages.error(request, "You are not enrolled in this course.")
        return redirect('home')


@login_required
def create_course(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = CourseForm(request.POST)
            if form.is_valid():
                course = form.save(commit=False)
                course.instructor = request.user
                course.save()
                messages.success(request, "Course created successfully.")
                return redirect('course_detail', course_id=course.id)
        else:
            form = CourseForm()
        return render(request, 'courses/create_course.html', {'form': form})
    else:
        messages.error(request, "You don't have permission to create courses.")
        return redirect('home')

@login_required
def create_lesson(request, course_id):
    if request.user.is_staff:
        course = get_object_or_404(Course, id=course_id, instructor=request.user)
        if request.method == 'POST':
            form = LessonForm(request.POST)
            if form.is_valid():
                lesson = form.save(commit=False)
                lesson.course = course
                lesson.save()
                messages.success(request, "Lesson created successfully.")
                return redirect('course_detail', course_id=course.id)
        else:
            form = LessonForm()
        return render(request, 'courses/create_lesson.html', {'form': form, 'course': course})
    else:
        messages.error(request, "You don't have permission to create lessons.")
        return redirect('home')

@login_required
def student_progress(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    context = {
        'enrollments': enrollments,
    }
    return render(request, 'courses/student_progress.html', context)

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        if Enrollment.objects.filter(student=request.user, course=course).exists():
            messages.warning(request, "You are already enrolled in this course.")
        else:
            Enrollment.objects.create(student=request.user, course=course)
            messages.success(request, f"You have successfully enrolled in {course.title}.")
        return redirect('course_detail', course_id=course.id)
    return render(request, 'courses/enroll_confirm.html', {'course': course})

