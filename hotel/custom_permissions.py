from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Guest

def create_custom_permissions(sender, **kwargs):
    content_type = ContentType.objects.get_for_model(Guest)
    if Permission.objects.filter(codename='view_sensitive_fields').exists():
        return
    Permission.objects.create(
        codename='view_sensitive_fields',
        name='Can view sensitive fields',
        content_type=content_type,
    )