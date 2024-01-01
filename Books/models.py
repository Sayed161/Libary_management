from django.db import models
from category.models import catagory
from django.contrib.auth.models import User
# Create your models here.

STAR = (
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5)
)

class Books(models.Model):
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=70)
    image = models.ImageField(upload_to='./media/image', blank=True,null=True)
    borrowing_price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ManyToManyField(catagory)
    is_borrowed = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    
class review(models.Model):
    books = models.ForeignKey(Books, on_delete = models.CASCADE,related_name="reviews")
    created = models.DateTimeField(auto_now_add=True)
    star = models.IntegerField(choices = STAR)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="reviews")