

from products.models import Category


def create_category(*, name, slug, parent=None, is_active=True) -> Category:
    return Category.objects.create(name=name, slug=slug, parent=parent, is_active=is_active)
    

def update_category(*, instance: Category, data: dict) -> Category:   
    for key, value in data.items():
        setattr(instance, key, value)
    instance.save()
    return instance