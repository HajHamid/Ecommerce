from products.models import Category

def get_parent_categories():
    """
    Returns a list of parent categories that have no parent themselves.
    """
    return Category.objects.filter(parent__isnull=True).order_by('name')