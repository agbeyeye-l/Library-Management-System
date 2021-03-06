from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# user account
class Account(models.Model):
    CHOICES = (
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="account")
    role = models.CharField(max_length=50, choices=CHOICES)
    heldBook = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def heldBooks(self):
        return self.heldBook

    def lendBookToUser(self):
        self.heldBook +=1
        self.save()

    def releaseBook(self):
        self.heldBook-=1
        self.save()


# signal to create an account for newly created user
@receiver(post_save, sender = User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
        
        


