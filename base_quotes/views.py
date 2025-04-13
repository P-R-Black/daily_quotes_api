from io import BytesIO
from django.views import View
from django.views.generic import TemplateView
from django.utils.text import slugify
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from datetime import date
from django.utils.timezone import localdate
from quotes_api.models import Author, Tag, Quote
import requests
import random
from django.http import JsonResponse
from django.core.cache import cache
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='downloaded_quotes.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'base_quotes/home.html'
    today = date.today()
    authors = Author.objects.all()
    tags = Tag.objects.all()
    selected_quote = None
    daily_quote = None


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = localdate()
        self.daily_quote = Quote.objects.filter(date_posted=today).first()

        if not self.daily_quote:
            daily_quote = cache.get('daily_quote')

        self.authors = Author.objects.all()
        self.tags = Tag.objects.all()

        # Store selected tag/author in session
        selected_value = self.request.GET.get('selected_value')

        if selected_value:
            if Tag.objects.filter(name__iexact=selected_value).exists():
                self.request.session['selected_tag'] = selected_value
                self.request.session['selected_author'] = None
            elif Author.objects.filter(name__iexact=selected_value).exists():
                self.request.session['selected_author'] = selected_value
                self.request.session['selected_tag'] = None

        context.update({
            'year': self.today.year,
            'tags': self.tags,
            'authors': self.authors,
            'daily_quote': self.daily_quote
        })

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        selected_value = request.GET.get('selected_value')

        if selected_value:
            if Tag.objects.filter(name__iexact=selected_value).exists():
                request.session['selected_tag'] = selected_value
                request.session['selected_author'] = None
            elif Author.objects.filter(name__iexact=selected_value).exists():
                request.session['selected_author'] = selected_value
                request.session['selected_tag'] = None

            # If this is an AJAX request, respond with JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'selected_value': selected_value})

        return self.render_to_response({
            'year': self.today.year,
            'tags': self.tags,
            'authors': self.authors,
            'daily_quote': self.daily_quote,
            'selected_quote': self.selected_quote
        })

        # return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        selected_tag = request.session.get('selected_tag')
        selected_author = request.session.get('selected_author')
        api_response = None


        if selected_tag:
            api_response = requests.get(f'http://localhost:8000/api/v1/quotes/{selected_tag}')
        elif selected_author:
            api_response = requests.get(f'http://localhost:8000/api/v1/quotes/author/{slugify(selected_author)}')

        if api_response:
            quotes = api_response.json().get('quotes', {}).get('results', [])
            self.selected_quote = random.choice(quotes) if quotes else None


        return self.render_to_response({
            'year': self.today.year,
            'tags': self.tags,
            'authors': self.authors,
            'selected_quote': self.selected_quote
        })


class AboutPageView(View):
    template_name = 'base_quotes/about.html'

    def get(self, request, *args, **kwargs):
        return self.handle_request(request)

    def post(self, request, *args, **kwargs):
        return self.handle_request(request)

    def handle_request(self, request):
        selected_value = request.POST.get('selected_value') or "President"
        api_by_tag = None

        if Tag.objects.filter(name__iexact=selected_value).exists():
            api_by_tag = requests.get(f'http://localhost:8000/api/v1/quotes/{slugify(selected_value)}')
        elif Author.objects.filter(name__iexact=selected_value).exists():
            api_by_tag = requests.get(f'http://localhost:8000/api/v1/quotes/author/{slugify(selected_value)}')

        if api_by_tag:
            full_api_by_tag = api_by_tag.json()

            tags_data = {
                "drfapi": full_api_by_tag['drfapi'],
                "info": full_api_by_tag['info'],
                "servers": full_api_by_tag['servers'],
                "external_docs": full_api_by_tag['external_docs'],
                "security": full_api_by_tag['security'],
                "count": full_api_by_tag['quotes']['count'],
                "next": full_api_by_tag['quotes']['next'],
                "previous": full_api_by_tag['quotes']['previous'],
                "results": full_api_by_tag['quotes']['results'],

            }
            return render(request, self.template_name, {'tags_data': tags_data})

        return render(request, self.template_name)

class DocsPageView(View):
    template_name = 'base_quotes/docs.html'

    def get(self, request, *args, **kwargs):
        return self.handle_request(request)

    def post(self, request, *args, **kwargs):
        return self.handle_request(request)

    def handle_request(self, request):
        return render(request, self.template_name)



def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"



def generate_image(request):
    INSTAGRAM_QUOTE_MARGIN_LEFT: int = 40
    INSTAGRAM_QUOTE_MARGIN_TOP: int = 20
    INSTAGRAM_QUOTE_MARGIN_RIGHT: int = 40
    INSTAGRAM_QUOTE_MARGIN_BOTTOM: int = 300
    INSTAGRAM_FONT_SIZE: int = 100
    INSTAGRAM_LINE_SPACING: int = 15

    TIKTOK_QUOTE_MARGIN_LEFT: int = 20
    TIKTOK_QUOTE_MARGIN_TOP: int = 20
    TIKTOK_QUOTE_MARGIN_RIGHT: int = 20
    TIKTOK_QUOTE_MARGIN_BOTTOM: int = 400
    TIKTOK_FONT_SIZE: int = 125
    TIKTOK_LINE_SPACING: int = 35


    if request.method == 'POST':
        get_post = request.POST
        image_style = get_post['image_style']
        background_color = get_post['background_color']
        font_color = get_post['font_color']
        quote = get_post['quote']
        author = get_post['author']
        shadow_option = get_post['shadow']
        font_style = get_post['font_style']

        # Log the download event
        logging.info(f'Download: "{image_style.lower()}" - "{quote}" - "{author}"')

        if image_style == "Instagram":
            width, height = 1080, 1080
            left_margin = INSTAGRAM_QUOTE_MARGIN_LEFT
            right_margin = INSTAGRAM_QUOTE_MARGIN_RIGHT
            top_margin = INSTAGRAM_QUOTE_MARGIN_TOP
            bottom_margin = INSTAGRAM_QUOTE_MARGIN_BOTTOM
            font_size = INSTAGRAM_FONT_SIZE
            line_spacing = INSTAGRAM_LINE_SPACING

        else: # TikTok Layout
            width, height = 1080, 1920
            left_margin = TIKTOK_QUOTE_MARGIN_LEFT
            right_margin = TIKTOK_QUOTE_MARGIN_RIGHT
            top_margin = TIKTOK_QUOTE_MARGIN_TOP
            bottom_margin = TIKTOK_QUOTE_MARGIN_BOTTOM
            font_size = TIKTOK_FONT_SIZE
            line_spacing = TIKTOK_LINE_SPACING


        text_area_width = width - (left_margin + right_margin)
        text_area_height = height - (top_margin + bottom_margin)

        if font_style == "Blinker":
            font_path =  "static/font/blinker/Blinker-Regular.ttf"
        else:
            font_path = "static/font/blinker/AbrilFatface-Regular.ttf"


        image = Image.new("RGB", (width, height), background_color)
        draw = ImageDraw.Draw(image)
        extra_spacing = line_spacing
        x_shadow, y_shadow, shadow_blur, shadow_opacity = parse_text_shadow(str(shadow_option))
        shadow_color = (0, 0, 0)

        fit_text_with_wrapping(draw, font_size, font_color, quote, author, font_path, text_area_width,
                               text_area_height, left_margin, right_margin, bottom_margin, extra_spacing,
                               x_shadow, y_shadow, shadow_blur, shadow_opacity, shadow_color)


        img_buffer = BytesIO()
        image.save(img_buffer, format="PNG")
        # image.show()
        img_buffer.seek(0)


        # Return image as HTTP Response
        response = HttpResponse(img_buffer, content_type='image/png')
        response["Content-Disposition"] = 'attachment; filename="daily_quote.png"'
        return response


    return HttpResponse(status=400)


def draw_blurred_text(draw, position, text, font, shadow_color, blur_radius):
    """Draw text with a blurred shadow effect."""
    x, y = position

    shadow_layer = Image.new("RGBA", draw.im.size, (0, 0, 0, 0))  # Transparent layer
    shadow_draw = ImageDraw.Draw(shadow_layer)



    for i in range(max(1, int(blur_radius))):
        # Apply increasing offsets for blur effect
        shadow_x = x + i
        shadow_y = y + i

        # Draw the shadow text on this separate image
        shadow_draw.text((shadow_x, shadow_y), text, font=font, fill=shadow_color)

    # Apply Gaussian Blur to the shadow
    blurred_shadow = shadow_layer.filter(ImageFilter.GaussianBlur(blur_radius))

    # Paste the blurred shadow onto the main image
    draw._image.paste(blurred_shadow, (0, 0), blurred_shadow)


def apply_shadow(draw, text, font, text_x, text_y, shadow_offset_x, shadow_offset_y, shadow_color, blur, opacity):

    # Convert shadow color to RGBA with opacity
    shadow_color_rgba = (shadow_color[0], shadow_color[1], shadow_color[2], int(opacity * 255))

    """Apply a shadow effect with blur and opacity."""
    shadow_x = text_x + shadow_offset_x
    shadow_y = text_y + shadow_offset_y

    # Use the new function to draw blurred text for shadow
    draw_blurred_text(draw, (shadow_x, shadow_y), text, font, shadow_color_rgba, blur)



def fit_text_with_wrapping(draw, img_font_size, img_font_color, text, author, font_path, max_width, max_height,
                           start_x, start_y, bottom_margin, extra_spacing, shadow_offset_x, shadow_offset_y,
                           shadow_blur, shadow_opacity, shadow_color):

    font_size = img_font_size
    font = ImageFont.truetype(font_path, font_size)

    # Adjust font size to fit within max_width and max_height
    while True:
        wrapped_lines = []  # Store lines after wrapping manually
        words = text.split()
        current_line = ""

        for word in words:
            test_line = current_line + " " + word if current_line else word
            line_width = font.getbbox(test_line)[2]

            if line_width <= max_width:
                current_line = test_line
            else:
                wrapped_lines.append(current_line)  # Commit current line
                current_line = word  # Start new line

        if current_line:
            wrapped_lines.append(current_line)

        # Calculate total text height
        total_text_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in wrapped_lines)

        if total_text_height <= max_height:
            break  # Stop if text fits
        else:
            font_size -= 1.5  # Reduce font size
            font = ImageFont.truetype(font_path, font_size)

    # Calculate Y position to center vertically
    text_y = start_y + (max_height - total_text_height) // 2


    # Draw each line centered horizontally
    for line in wrapped_lines:
        line_width = font.getbbox(line)[2]
        text_x = start_x + (max_width - line_width) // 2  # Center each line

        # Draw Shadow
        apply_shadow(draw, line, font, text_x, text_y, shadow_offset_x, shadow_offset_y, shadow_color, shadow_blur, shadow_opacity)

        # Now draw the actual text
        draw.text((text_x, text_y), line, font=font, fill=img_font_color)
        text_y += (font.getbbox(line)[3] - font.getbbox(line)[1]) + extra_spacing

    # Now add the author below
    author_font_size = font_size // 1.5  # Make author name smaller than quote
    author_font = ImageFont.truetype(font_path, author_font_size)

    author_width = author_font.getbbox(author)[2]
    author_x = start_x + (max_width - author_width) // 2
    author_y = start_y + max_height + 150  # Place it just below the quote with padding

    # Ensure the author fits within the bottom margin
    if author_y + author_font.getbbox(author)[3] > start_y + max_height + bottom_margin:
        author_font_size -= 2
        author_font = ImageFont.truetype(font_path, author_font_size)
        author_width = author_font.getbbox(author)[2]
        author_x = start_x + (max_width - author_width) // 2  # Recalculate center


    # Draw author's shadow first
    apply_shadow(draw, author, author_font, author_x, author_y, shadow_offset_x, shadow_offset_y, shadow_color,
                 shadow_blur, shadow_opacity)


    # Now draw the author's actual name
    draw.text((author_x, author_y), author, font=author_font, fill=img_font_color)

    # Return the final font size and text height for reference
    return font_size, total_text_height


def parse_text_shadow(text_shadow):

    shadows = text_shadow.split()

    if len(shadows) < 4:
        raise ValueError(f"Invalid text shadow format: {text_shadow}. Expected 4 components")

    x_offset = float(shadows[0].strip('px'))
    y_offset = float(shadows[1].strip('px'))
    blur = float(shadows[2].strip('px'))
    opacity = float(shadows[-1].strip(")"))


    return x_offset, y_offset, blur, opacity


