from django.utils.safestring import mark_safe


class ImageMixins():
    def image_snapshot(self, instance):
        if instance.image and instance.image.url:
            return mark_safe(
                f'<img src="{instance.image.url}" width="64" height="64"/>'
                )
        return mark_safe('Image missing')
