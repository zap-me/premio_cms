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



class LocationPromotion(models.Model):
    '''
    Location Promotion Data - has M2M relationship with LocationPage
    '''
    promotion_type=models.CharField(max_length=1) #one letter char, treat like enum
    



class LocationPage(Page):
    '''
    Location Page Data - M2M relationship with LocationPromotion
    '''
    date = models.DateField("Creation date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=LocationPageTag, blank=True)
    lat_long = models.CharField(max_length=25, default='0,0') 
    latitude=models.FloatField(blank=True)
    longitude=models.FloatField(blank=True)
    promotions=models.ManyToManyField(LocationPromotion)
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
            FieldPanel('lat_long'),
        ], heading="Location information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    def save(self, *args, **kwargs):
        self.latitude=round(float(self.lat_long.split(",")[0]),6)
        self.longitude=round(float(self.lat_long.split(",")[1]),6)
        super(LocationPage, self).save(*args, **kwargs)


    def __str__(self):
        return "date | {0} into | {1} body| {2} tags | {3} lat_long | {4} latitude | {5} longitude | {6} body | {7} promotions | {8}".format(self.date,self.intro,self.body,self.tags,self.lat_long,self.latitude,self.longitude,self.promotions)


    def __repr__(self):
        return "date | {0} into | {1} body| {2} tags | {3} lat_long | {4} latitude | {5} longitude | {6} body | {7} promotions | {8}".format(self.date,self.intro,self.body,self.tags,self.lat_long,self.latitude,self.longitude,self.promotions)

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

