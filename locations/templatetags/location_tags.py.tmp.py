from django import template

from locations.models import LocationCarousel, LocationPage

register = template.Library()

# LocationCarousel snippet 



@register.inclusion_tag('locations/tags/location_carousel.html', takes_context=True)
def locationcarousels(context):

    return {
        'locationcarousels' : LocationCarousel.objects.all(),
        'request' : context['request'],
    }


