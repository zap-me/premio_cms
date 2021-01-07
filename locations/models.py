from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

class LocationsIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published locations
        context = super().get_context(request)
        locationpages = self.get_children().live()
        context['locationpages'] = locationpages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

class LocationPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'LocationPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class LocationPage(Page):
    date = models.DateField("Creation date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=LocationPageTag, blank=True)
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('latitude'),
            FieldPanel('longitude'),
        ], heading="Location information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

class LocationPageGalleryImage(Orderable):
    page = ParentalKey(LocationPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

class LocationTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        locationpages = LocationPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['locationpages'] = locationpages
        return context
