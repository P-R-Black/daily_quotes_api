from django.core.management.base import BaseCommand

import csv
from quotes_api.models import Quote, Author, Tag

class Command(BaseCommand):
    help = 'import booms'

    print('help', help)

    def handle(self, *args, **kwargs):
        TAG_STANDARDIZATION = {
            "women": "women voices",
            "woman": "women voices",
            "philosopher": "philosophy",
            "black": "black voices"
        }
        with open('/Users/paulblack/PycharmProjects/Projects/DailyQuotes/used_quotes.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='|')


            for row in reader:
                if len(row) < 3:
                    continue

                text, author_name, tag_names = row[0].strip(), row[1].strip(), row[2:]
                author, _ = Author.objects.get_or_create(name=author_name)
                quote, created = Quote.objects.get_or_create(text=text, author=author)

                for tag_name in tag_names:
                    tag_name = tag_name.strip().lower()
                    tag_name = TAG_STANDARDIZATION.get(tag_name, tag_name)
                    if tag_name:
                        tag, _ =  Tag.objects.get_or_create(name=tag_name)
                        quote.tags.add(tag)


                quote.save()