from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
# Create your models here.

class Post(models.Model):
    # Connecting an author to an actual authorization User (superuser)
    # So when I create a superuser, he'll be able to author a new post
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)
    # blank = True maybe you don't wanna publish it yet
    # null = True maybe you don't have a publication date whatsoever

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    # reserved function name
    def get_absolute_url(self):
        # What should I do once I create an instance of Post
        return reverse("post_detail",kwargs={'pk':self.pk})
        # kwargs is a keyword agrument dictinary where the primary key matches up with self.pk
        # after creating a post, go to post_detail page for the primary key for the post you just create_date

    # The string representation for my Post model
    def __str__(self):
        return self.title


class Comment(models.Model):
    # Connecting each comment to an actual post
    post = models.ForeignKey('blog.Post',related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    # Once the comment should be approved by a superuser
    # it doesn't make sense to go back to the list of the comments
    # So instead, go back to the list of all the posts
    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text
