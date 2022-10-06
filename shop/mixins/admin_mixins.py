from django.utils.safestring import mark_safe


class ImageMixins():
    def image_snapshot(self, instance):
        return mark_safe(
            f'<img src="{instance.image.url}" width="64" height="64"/>'
            )
