
from products.models import Brand

def get_active_brands():
    return Brand.objects.filter(is_active=True)