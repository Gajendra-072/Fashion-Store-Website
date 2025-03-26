import os
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.cache import cache

UNSPLASH_ACCESS_KEY = 'Fe5k1006bU61Iyd_v8t3_YDHoL25mi6UBxPCEVMkfR8'

def get_single_image(query, fallback_path='store/static/store/images/fallback.jpg'):
    """
    Get a single image from Unsplash API with caching
    """
    cache_key = f'unsplash_image_{query}'
    cached_image = cache.get(cache_key)
    
    if cached_image:
        return cached_image
    
    # Check if we have a fallback image
    if default_storage.exists(fallback_path):
        return default_storage.url(fallback_path)
    
    # If no fallback image exists, create one
    try:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(fallback_path), exist_ok=True)
        
        # Create a simple fallback image
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (800, 600), color='#f0f0f0')
        d = ImageDraw.Draw(img)
        d.text((400, 300), "No Image Available", fill='#666666', anchor="mm")
        
        # Save the image
        img_path = default_storage.save(fallback_path, ContentFile(img.tobytes()))
        return default_storage.url(img_path)
    except Exception as e:
        print(f"Error creating fallback image: {e}")
        return None

def get_fashion_image(category, query=None):
    """
    Fetch a fashion image from Unsplash API
    category: str - The category of image (e.g., 'men-clothing', 'women-shoes')
    query: str - Optional specific search query
    """
    cache_key = f'fashion_image_{category}_{query}'
    cached_image = cache.get(cache_key)
    
    if cached_image:
        return cached_image

    base_url = 'https://api.unsplash.com/photos/random'
    headers = {
        'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'
    }
    
    # Enhanced queries for better fashion results with specific styles
    default_queries = {
        'men-clothing': 'men online shopping fashion clothing ecommerce',
        'women-clothing': 'women fashion clothing street style casual wear',
        'men-shoes': 'men shoes sneakers fashion streetwear',
        'women-shoes': 'women shoes heels fashion streetwear',
        'men-accessories': 'men fashion accessories watch jewelry streetwear',
        'women-accessories': 'women fashion accessories jewelry bag streetwear'
    }
    
    params = {
        'query': query or default_queries.get(category, 'fashion street style'),
        'orientation': 'portrait',
        'count': 1,
        'content_filter': 'high',  # Get high-quality images
        'collections': '317099,9691100,317099'  # Fashion and ecommerce collections
    }
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            image_url = data[0]['urls']['regular']
            # Cache the result for 24 hours
            cache.set(cache_key, image_url, 60 * 60 * 24)
            return image_url
    except Exception as e:
        print(f"Error fetching image from Unsplash: {e}")
    
    # Fallback to a default image if API fails
    return f"{settings.STATIC_URL}images/default-fashion.jpg"

def get_category_images(category, count=4):
    """
    Fetch multiple images for a category
    """
    cache_key = f'category_images_{category}_{count}'
    cached_images = cache.get(cache_key)
    
    if cached_images:
        return cached_images

    base_url = 'https://api.unsplash.com/photos/random'
    headers = {
        'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'
    }
    
    # Enhanced queries for better fashion results with specific styles
    default_queries = {
        'men-clothing': 'men online shopping fashion clothing ecommerce',
        'women-clothing': 'women fashion clothing street style casual wear',
        'men-shoes': 'men shoes sneakers fashion streetwear',
        'women-shoes': 'women shoes heels fashion streetwear',
        'men-accessories': 'men fashion accessories watch jewelry streetwear',
        'women-accessories': 'women fashion accessories jewelry bag streetwear'
    }
    
    params = {
        'query': default_queries.get(category, 'fashion street style'),
        'orientation': 'portrait',
        'count': count,
        'content_filter': 'high',  # Get high-quality images
        'collections': '317099,9691100,317099'  # Fashion and ecommerce collections
    }
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list):
            image_urls = [item['urls']['regular'] for item in data]
            # Cache the result for 24 hours
            cache.set(cache_key, image_urls, 60 * 60 * 24)
            return image_urls
    except Exception as e:
        print(f"Error fetching images from Unsplash: {e}")
    
    # Fallback to default images if API fails
    return [f"{settings.STATIC_URL}images/default-fashion.jpg"] * count 