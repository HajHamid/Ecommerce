from products.models import Brand


def create_brand(*, name, image='default.png', is_active=True) -> Brand:
    return Brand.objects.create(
        name=name,
        image=image,
        is_active=is_active
    )


def update_brand(*, instance: Brand, data: dict) -> Brand:
    for key, value in data.items():
        setattr(instance, key, value)
    instance.save()
    return instance
        