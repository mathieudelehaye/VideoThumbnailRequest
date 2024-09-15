import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class ThumbnailRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.TextField()
    reference_image = models.ImageField(upload_to='reference_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail_file = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.idea[:30]}"
    
    # Override the delete method to remove both images (reference and thumbnail)
    def delete(self, *args, **kwargs):
        # Delete the reference image if it exists
        if self.reference_image:
            if os.path.isfile(self.reference_image.path):
                os.remove(self.reference_image.path)

        # Delete the uploaded thumbnail if it exists
        if self.thumbnail_file:
            if os.path.isfile(self.thumbnail_file.path):
                os.remove(self.thumbnail_file.path)

        # Call the super class's delete method to ensure the object is deleted from the database
        super().delete(*args, **kwargs)

# Signal to delete both the reference image and the uploaded thumbnail when a ThumbnailRequest is deleted
@receiver(pre_delete, sender=ThumbnailRequest)
def delete_related_files(sender, instance, **kwargs):
    # Delete the reference image if it exists
    if instance.reference_image:
        if os.path.isfile(instance.reference_image.path):
            os.remove(instance.reference_image.path)

    # Delete the uploaded thumbnail if it exists
    if instance.thumbnail_file:
        if os.path.isfile(instance.thumbnail_file.path):
            os.remove(instance.thumbnail_file.path)