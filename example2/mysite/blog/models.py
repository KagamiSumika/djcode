from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    title = models.CharField(max_length=250) #这是文章标题字段。这个字段被设置为Charfield类型，在SQL数据库中对应VARCHAR数据类型
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')   #该字段通常在URL中使用，unique_for_date表示不允许有两条记录的publish字段日期和title字段全都相同
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')  #通过这个外键，告诉Django一文章只有一个作者，一个作者可以多篇文章。on_delete表示删除外键关联时候的操作。CASCADE意味删除一个作者则删除全文章。
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    object = models.Manager() #默认的管理器
    published = PublishedManager()  #自定义的管理器
    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

class Meta:
    ordering = ('-publish',)

def __str__(self):
    return self.title

