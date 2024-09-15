from django.contrib import admin
from django.utils.html import mark_safe
from .models import ThumbnailRequest

class ThumbnailRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'idea', 'status', 'created_at', 'reference_image_display', 'thumbnail_file_display', 'reference_image_path')

    def reference_image_display(self, obj):
        if obj.reference_image:
            return mark_safe(f'<img src="{obj.reference_image.url}" width="100" />')
        return "No Image"
    
    def thumbnail_file_display(self, obj):
        if obj.thumbnail_file:
            return mark_safe(f'<img src="{obj.thumbnail_file.url}" width="100" />')
        return "No Thumbnail Uploaded"

    def reference_image_path(self, obj):
        if obj.reference_image:
            return obj.reference_image.url
        return "No Image"

    # Automatically update the status when the thumbnail is uploaded
    def save_model(self, request, obj, form, change):
        if obj.thumbnail_file and obj.status != 'DONE':
            obj.status = 'DONE'  # Automatically set status to "Done"
        super().save_model(request, obj, form, change)

    reference_image_display.short_description = 'Reference Image'
    thumbnail_file_display.short_description = 'Thumbnail'
    reference_image_path.short_description = 'Image Path'

admin.site.register(ThumbnailRequest, ThumbnailRequestAdmin)
