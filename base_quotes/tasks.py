import random
from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from django.utils.timezone import localdate
import logging

from quotes_api.models import Quote

logger = logging.getLogger(__name__)
logging.basicConfig(filename='daily_quotes.log', level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

@shared_task
def set_daily_quote():
    quote = Quote.objects.order_by('?').first()
    today = localdate()
    print('set_daily_quote | quote', quote)
    logger.debug(f'set_daily_quote | {quote}')

    if quote:
        print(f'Daily quote already in cache: {quote.text} - {quote.author.name}')
        quote.date_posted = today
        quote.save()

        # Cache the daily quote with a 24-hour expiration
        cache.set('daily_quote', quote, timeout=0)
        print(f'Daily quote set: {quote.text} - {quote.author.name}')
        return f'Daily quote set: {quote.text} - {quote.author.name}'

    else:
        logger.debug('No quotes found to set as daily quote')
        return 'No quotes found to set as daily quote'
