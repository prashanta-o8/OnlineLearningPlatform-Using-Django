from django import template
from courses.models import Progress

register = template.Library()

@register.filter
def completed_by(lesson, user):
    return Progress.objects.filter(student=user, lesson=lesson, completed=True).exists()