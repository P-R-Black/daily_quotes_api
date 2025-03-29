from rest_framework.response import Response


class MetadataMixin:
    def get_metadata(self, serialized_data):
        return {
            "drfapi": "1.0.0",
            "info": {
                "title": "Daily Quotes API",
                "version": "1.0.0",
                "description": "This is the public API for Daily Quotes"
            },
            "servers": [
                {"url": "/api/v1"}
            ],
            "external_docs": {
                "url": "https://www.dailyquotesapi.paulrblack.com/",
                "description": "Access to interesting, comical and inspirational quotes"
            },
            "security": [
                {
                    "client_id": [],
                    "client_secret": []
                }
            ],
            "quotes": serialized_data  # Add the actual drinks data here
        }