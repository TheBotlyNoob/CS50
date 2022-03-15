from django import template

register = template.Library()


@register.filter
def get_current_bid(listing):
    return listing.bids.latest("amount")


@register.filter
def get_bids(listing):
    return listing.bids.all()