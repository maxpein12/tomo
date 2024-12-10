from celery import shared_task
from django.core.cache import cache
from .models import Users

@shared_task
def update_cache():
    # Get the user's status from the database
    users = Users.objects.all()
    user_statuses = [(user.id, user.status) for user in users]

    # Update the cache
    cache.set('user_statuses', user_statuses)