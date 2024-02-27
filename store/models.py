from django.db import models
from django.core.exceptions import ValidationError


def validate_image(image):
    file_size = image.size
    limit_mb = 5
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("Max size of file is %s MB" % limit_mb)


# Create your models here.
class Store(models.Model):
    fullname = models.CharField(max_length=20)
    phone = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=255)
    store_name = models.CharField(max_length=20)
    store_logo = models.ImageField(
        upload_to="stores_logo/", validators=[validate_image], default="stores_logo/default_logo.png")
    store_backgroung = models.ImageField(upload_to="stores_background/", validators=[
                                         validate_image], default="stores_background/default_background.jpg")
    stores_cat = models.ForeignKey(
        'controller.Categories', on_delete=models.PROTECT)
    storelat = models.DecimalField(max_digits=9, decimal_places=7)
    storelong = models.DecimalField(max_digits=10, decimal_places=7)
    # date_created = models.DateTimeField(blank=True,null=True,auto_now_add=True )
    date_updated = models.DateTimeField(blank=True, null=True, auto_now=True)
    open = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.fullname

    class Meta:
        ordering = ["-date_updated"]

    # def save(self, *args, **kwargs):
    #     if self.password:
    #         self.password =
    #     super(Store, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=10)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="category")
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name + "_" + self.store.store_name

    def add_item(self):
        self.count += 1
        self.save()

    def remove_item(self):
        if self.count > 0:
            self.count -= 1
            self.save()

    class Meta:
        unique_together = ('name', 'store')


class Item(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    price = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="items_image/",
                              validators=[validate_image])
    active = models.BooleanField(default=True)
    store = models.ForeignKey(
        Store, on_delete=models.PROTECT, related_name="Delivery_items")
    cat = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="Delivery_items")
    likes = models.PositiveIntegerField(default=0)
    selling = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name + "_" + self.store.store_name

    def add_like(self):
        self.likes += 1
        self.save()

    def remove_like(self):
        if self.likes > 0:
            self.likes -= 1
            self.save()

    def add_sell(self):
        self.selling += 1
        self.save()

    class Meta:
        unique_together = ('name', 'store')
