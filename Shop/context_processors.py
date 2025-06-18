# shop/context_processors.py
from .models import SiteInfo
from datetime import datetime

def site_info(request):
    try:
        # Get the active site configuration
        config = SiteInfo.objects.filter(active=True).first()
        
        if not config:
            # Return defaults if no configuration exists
            return {
                'SITE_LOGO_NAME': 'aiQuest',
                'SITE_NAME': 'aiQuest E-Commerce',
                'COMPANY_NAME': 'aiQuest Technologies',
                'YEAR': datetime.now().year,
                'LOGO_IMAGE': None
            }
            
        return {
            'SITE_LOGO_NAME': config.logo_name,
            'SITE_NAME': config.site_name,
            'COMPANY_NAME': config.company_name,
            'YEAR': datetime.now().year,
            'LOGO_IMAGE': config.logo_image.url if config.logo_image else None
        }
    except:
        # Fallback in case of any error
        return {
            'SITE_LOGO_NAME': 'aiQuest',
            'SITE_NAME': 'aiQuest E-Commerce',
            'COMPANY_NAME': 'aiQuest Technologies',
            'YEAR': datetime.now().year,
            'LOGO_IMAGE': None
        }