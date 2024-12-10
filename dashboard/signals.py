from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender='dashboard.Users')
def invalidate_cache_on_user_status_change(sender, instance, created, **kwargs):
    # Send a message to the WebSocket endpoint
    from channels import Group
    Group('user-status').send({
        'text': 'User status changed',
    })