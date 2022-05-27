from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Author(models.Model):
    raiting = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):

        article = 0
        comments = 0
        comments_author = 0

        post_cash = Post.object.filter(author=self.user).values('raiting')
        for i in post_cash:
            article += int(i['raiting'])

        comments_author_cash = Comment.object.filter(author=self.user).values('raiting')
        for i in comments_author_cash:
            comments_author += int(i['raiting'])

        comments_cash = Comment.object.filter(post__author=self.user).values('raiting')
        for i in comments_cash:
            comments += int(i['raiting'])

        self.raiting = article + comments + comments_author
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


POSTLIST = [
    ('AR', 'article'),
    ('NE', 'news')
    ]


class Post(models.Model):
    article = models.CharField(max_length=2, choices=POSTLIST, default='ar')
    data = models.DateTimeField(auto_now_add=True)
    head = models.CharField(max_length=255)
    body = models.TextField()
    raiting = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.raiting + 1
        self.save()

    def dislike(self):
        self.raiting - 1
        self.save()

    def preview(self):
        return self.body[0:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    raiting = models.IntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def like(self):
        self.raiting + 1
        self.save()

    def dislike(self):
        self.raiting - 1
        self.save()
