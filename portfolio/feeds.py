from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from core.models import Work

from django.utils.feedgenerator import Atom1Feed


class RssWorkFeeds(Feed):
    title = "Works"
    link = "/latestworks/"
    description = "Recent and brief Description for ANINDA KUNDU"
    
    def items(self):
        return Work.objects.order_by("-modified_at")[:100]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.description
    
    def item_lastupdated(self, item):
        return item.modified_at

class AtomWorkFeed(RssWorkFeeds):
    feed_type = Atom1Feed
    subtitle = "RssWorkFeeds.description"
      