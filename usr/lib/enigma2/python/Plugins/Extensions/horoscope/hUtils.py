#!/usr/bin/python
# -*- coding: utf-8 -*-

import ssl
import time
from sys import version_info
from os import makedirs, listdir, unlink
from os.path import exists, join, getmtime, isfile
from . import plugin_path

if version_info[0] == 3:
    from urllib.request import urlopen, Request
else:
    from urllib2 import urlopen, Request


def get_country_code_for_horoscope(country_name):
    """
    Get country code for horoscope language/country names.
    This maps horoscope language names to country codes.
    """
    if not country_name:
        return ""
    
    # Map horoscope language names to FLAG CODES (not country codes)
    # Using flagcdn.com country codes
    flag_map = {
        "Arabic": "sa",           # Saudi Arabia flag
        "Azerbaijani": "az",      # Azerbaijan
        "Brazilian": "br",        # Brazil
        "Bulgarian": "bg",        # Bulgaria
        "Chinese": "cn",          # China
        "Czech": "cz",            # Czech Republic
        "Danish": "dk",           # Denmark
        "Dutch": "nl",            # Netherlands
        "English": "gb",          # United Kingdom
        "Finish": "fi",           # Finland (corrected from 'Finish' to 'fi')
        "French": "fr",           # France
        "German": "de",           # Germany
        "Greek": "gr",            # Greece
        "Hebrew": "il",           # Israel
        "Hindi": "in",            # India
        "Hungarian": "hu",        # Hungary
        "Italian": "it",          # Italy
        "Japanese": "jp",         # Japan
        "Korean": "kr",           # South Korea
        "Malay": "my",            # Malaysia
        "Norwegian": "no",        # Norway
        "Persian": "ir",          # Iran
        "Polish": "pl",           # Poland
        "Portuguese": "pt",       # Portugal
        "Romanian": "ro",         # Romania
        "Slovak": "sk",           # Slovakia
        "Slovenian": "si",        # Slovenia
        "Spanish": "es",          # Spain
        "Swedish": "se",          # Sweden
        "Thai": "th",             # Thailand
        "Turkish": "tr",          # Turkey
        "Vietnamese": "vn",       # Vietnam
    }
    
    # Exact match
    if country_name in flag_map:
        return flag_map[country_name]
    
    # Handle typo in original code ("Finish" should be "Finnish")
    if country_name.lower() == "finish":
        return "fi"
    
    return ""


def get_screen_width():
    """Get current screen width for flag size"""
    try:
        from enigma import getDesktop
        desktop = getDesktop(0)
        width = desktop.size().width()
        return width
    except:
        return 1920  # Default FHD

    
def download_flags(country_name, cache_dir="/tmp/horoscope_flags"):
    """
    Download flag for horoscope country/language.
    Returns: (success, flag_path)
    """
    try:
        # Get country code
        country_code = get_country_code_for_horoscope(country_name)
        if not country_code:
            print("[hUtils] No country code for:", country_name)
            return False, ""
        
        # Get screen width
        screen_width = get_screen_width()
        
        # Determine flag size based on screen resolution
        # Set dimensions based on screen size
        if screen_width >= 2560:      # WQHD
            width, height = 80, 60
        elif screen_width >= 1920:    # FHD
            width, height = 60, 45
        else:                         # HD
            width, height = 40, 30
        
        # Download with correct dimensions
        url = "https://flagcdn.com/%dx%d/%s.png" % (width, height, country_code.lower())
        
        # Create cache directory
        if not exists(cache_dir):
            try:
                makedirs(cache_dir)
            except:
                pass
        
        # Cache file path
        cache_file = join(cache_dir, "%s.png" % country_code.lower())
        
        # Check cache (1 week validity)
        if exists(cache_file):
            try:
                file_age = time.time() - getmtime(cache_file)
                if file_age < 604800:  # 7 days
                    print("[hUtils] Cache HIT:", country_name)
                    return True, cache_file
            except:
                pass
        
        # Build URL
        url = "https://flagcdn.com/%dx%d/%s.png" % (width, height, country_code.lower())
        print("[hUtils] Downloading flag for %s from: %s" % (country_name, url))
        
        # Download flag
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
        
        if version_info[0] == 3:
            # Python 3 with SSL context
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            req = Request(url, headers=headers)
            try:
                response = urlopen(req, timeout=10, context=ssl_context)
            except Exception as e:
                print("[hUtils] Error downloading flag:", e)
                return False, str(e)
        else:
            # Python 2
            req = Request(url, headers=headers)
            try:
                response = urlopen(req, timeout=10)
            except Exception as e:
                print("[hUtils] Error downloading flag:", e)
                return False, str(e)
        
        if response.getcode() != 200:
            return False, "HTTP %d" % response.getcode()
        
        # Read and save flag
        flag_data = response.read()
        
        with open(cache_file, 'wb') as f:
            f.write(flag_data)
        
        print("[hUtils] Flag saved:", cache_file)
        return True, cache_file
        
    except Exception as e:
        print("[hUtils] Error in download_flags:", e)
        return False, str(e)


def initialize_flags(cache_dir="/tmp/horoscope_flags"):
    """Initialize cache with any local flags if available"""
    local_dir = join(plugin_path, "countries")
    
    if not exists(local_dir):
        return 0
    
    if not exists(cache_dir):
        try:
            makedirs(cache_dir)
        except:
            pass
    
    copied = 0
    if exists(local_dir):
        for filename in listdir(local_dir):
            if filename.lower().endswith('.png'):
                src = join(local_dir, filename)
                dst = join(cache_dir, filename.lower())
                
                try:
                    import shutil
                    shutil.copy2(src, dst)
                    copied += 1
                except:
                    pass
    
    return copied


def cleanup_cache(max_age_days=7, cache_dir="/tmp/horoscope_flags"):
    """Clean old cached flags"""
    if not exists(cache_dir):
        return 0
    
    now = time.time()
    max_age = max_age_days * 86400
    removed = 0
    
    try:
        for filename in listdir(cache_dir):
            filepath = join(cache_dir, filename)
            if isfile(filepath):
                try:
                    file_age = now - getmtime(filepath)
                    if file_age > max_age:
                        unlink(filepath)
                        removed += 1
                except:
                    pass
    except:
        pass
    
    return removed
