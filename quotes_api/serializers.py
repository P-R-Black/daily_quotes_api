from rest_framework import serializers
from quotes_api.models import Quote, Author, Tag


class QuotesSerializerV1(serializers.ModelSerializer):
    text = serializers.CharField()
    name = serializers.CharField(source="author.name")
    # tags = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    # tag_names = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Quote
        fields = [
            'id', 'text', 'name', # 'tags', 'tag_names'
        ]

    def get_tag_names(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def create(self, validated_data):
        author_name = validated_data.pop("author")["name"]
        tag_names = validated_data.pop("tags", [])

        # Get or create author
        author, _ = Author.objects.get_or_create(name=author_name)

        # Create quote without tags first
        quote = Quote.objects.create(author=author, **validated_data)

        # Add tags to quote
        for tag_name in tag_names:
            tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
            quote.tags.add(tag_obj)

        return quote
