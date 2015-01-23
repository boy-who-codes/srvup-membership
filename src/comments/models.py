from django.db import models

# Create your models here.
from accounts.models import MyUser
from videos.models import Video


class CommentManager(models.Manager):
	def all(self):
		return super(CommentManager, self).filter(active=True).filter(parent=None)

	def create_comment(self, user=None, text=None, path=None, video=None):
		if not path:
			raise ValueError("Must include a path when adding a Comment")
		if not user:
			raise ValueError("Must include a user when adding a Comment")

		comment = self.model(
			user = user,
			path = path, 
			text = text
		)
		if video is not None:
			comment.video = video
		comment.save(using=self._db)
		return comment


class Comment(models.Model):
	user = models.ForeignKey(MyUser)
	parent = models.ForeignKey("self", null=True, blank=True)
	path = models.CharField(max_length=350)
	video = models.ForeignKey(Video, null=True, blank=True)
	text = models.TextField()
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	active = models.BooleanField(default=True)

	objects = CommentManager()

	class Meta:
		ordering = ['-timestamp']

	def __unicode__(self):
		return self.user.username

	@property
	def get_comment(self):
		return self.text

	@property
	def is_child(self):
		if self.parent is not None:
			return True
		else:
			return False

	def get_children(self):
		if self.is_child:
			return None
		else:
			return Comment.objects.filter(parent=self)



