from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.admin.edit_handlers import PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

def geo_coords_dist(lat1, lon1, lat2, lon2):
    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def str2latlon(s):
    lat = lon = 0
    parts = s.split(',')
    if len(parts) == 2:
        try:
            lat = float(parts[0])
            lon = float(parts[1])
        except ValueError:
            pass
    return lat, lon

class LocationsIndexPage(Page):
    promotion_title=models.CharField(max_length=100, default="promotion title goes here")
    promotion_description=models.CharField(max_length=250, default="promotion desscription goes here")
    intro = RichTextField(blank=True)
    show_near_me = models.BooleanField(default=True)
    max_dist_km = models.IntegerField(default=50, verbose_name='maximum distance (km)')

    def get_context(self, request):
        context = super().get_context(request)
        # tags
        tags = {}
        for tag in  Tag.objects.all():
            tags[tag] =  LocationPage.objects.filter(tags__name=tag).live()
        context['locationpagetags'] = tags
        # locations near me
        locationsnearme = []
        if 'geo' in request.COOKIES:
            lat, lon = str2latlon(request.COOKIES['geo'])
            if lat and lon:
                pages = LocationPage.objects.all().live()
                for page in pages:
                    page_lat, page_lon = str2latlon(page.lat_long)
                    if page_lat and page_lon:
                        d = geo_coords_dist(lat, lon, page_lat, page_lon)
                        if d <= self.max_dist_km:
                            locationsnearme.append(page)
        context['locationsnearme'] = locationsnearme
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('promoted_pages', label="Promoted Locations"),
        MultiFieldPanel([
            FieldPanel('show_near_me'),
            FieldPanel('max_dist_km'),
            FieldPanel('promotion_title'),
            FieldPanel('promotion_description'),
        ], heading='Locations near me'),
    ]

class LocationsIndexPromotedPage(Orderable):
    page = ParentalKey(LocationsIndexPage, on_delete=models.CASCADE, related_name='promoted_pages')
    promoted_page = models.ForeignKey(
        'wagtailcore.Page', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        PageChooserPanel('promoted_page', ['locations.LocationPage']),
        FieldPanel('caption'),
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
    lat_long = models.CharField(blank=True, max_length=30, verbose_name='Latitude, longitude')

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
            FieldPanel('lat_long', heading='this seems to be ignored in favor of the field "name" or "verbose_name"'),
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
        locationpages = LocationPage.objects.filter(tags__name=tag).live()

        # Update template context
        context = super().get_context(request)
        context['locationpages'] = locationpages
        return context
