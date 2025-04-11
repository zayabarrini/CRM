#!/usr/bin/env python3
import sys
import os
from pathlib import Path
import yaml
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('translation.log'),
        logging.StreamHandler()
    ]
)

# Configure paths
TRANSLATION_FUNCTIONS_PATH = "/home/zaya/Documents/Gitrepos/Linktrees/Business/Dev/Py/Transliteration/transliteration"
sys.path.append(TRANSLATION_FUNCTIONS_PATH)
try:
    from translationFunctions import translate_text
except ImportError as e:
    logging.error(f"Error importing translation functions: {e}")
    sys.exit(1)

# Supported languages
LANGUAGES = {
    'en': {'name': 'English', 'native': 'English'},
    'es': {'name': 'Spanish', 'native': 'Español'},
    'fr': {'name': 'French', 'native': 'Français'},
    'de': {'name': 'German', 'native': 'Deutsch'},
    'it': {'name': 'Italian', 'native': 'Italiano'},
    'ru': {'name': 'Russian', 'native': 'Русский'},
    'zh-ch': {'name': 'Chinese', 'native': '中文'},
    'jp': {'name': 'Japanese', 'native': '日本語'},
    'hi': {'name': 'Hindi', 'native': 'हिन्दी'},
    'ar': {'name': 'Arabic', 'native': 'العربية'},
    'ko': {'name': 'Korean', 'native': '한국어'}
}

class HTMLTranslator:
    def __init__(self):
        self.translation_cache = {}

    def extract_html_content(self, html_path):
        """Improved extraction for your specific HTML structure"""
        with open(html_path, 'r') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        content = {
            'title': soup.h1.get_text() if soup.h1 else '',
            'sections': [],
            'links': []
        }

        # Extract main sections
        sections = [
            ('intro', soup.find(class_='intro')),
            ('highlight', soup.find(class_='highlight')),
            ('collaborations', soup.find(class_='checklist').find_parent()),
            ('contact', soup.find(class_='signature').find_previous('p'))
        ]

        for name, section in sections:
            if section:
                content['sections'].append({
                    'title': name.capitalize(),
                    'body': '\n'.join(
                        elem.get_text().strip() 
                        for elem in section.find_all(['p', 'li'])
                        if elem.get_text().strip()
                    )
                })

        # Extract links
        for link in soup.find_all('a', href=True):
            content['links'].append({
                'text': link.get_text().strip(),
                'href': link['href']
            })

        return content

    def translate_content(self, content, target_lang):
        """Translate content while preserving structure"""
        if target_lang in self.translation_cache:
            return self.translation_cache[target_lang]

        try:
            translated = {
                'title': str(translate_text(content['title'], target_lang)),
                'sections': [],
                'links': content['links']  # Don't translate URLs
            }

            for section in content['sections']:
                translated['sections'].append({
                    'title': str(translate_text(section['title'], target_lang)),
                    'body': str(translate_text(section['body'], target_lang))
                })

            self.translation_cache[target_lang] = translated
            return translated

        except Exception as e:
            logging.warning(f"Translation failed for {target_lang}: {str(e)}")
            raise

    def generate_translations(self, html_path, output_path):
        """Generate multilingual YAML file"""
        try:
            source_content = self.extract_html_content(html_path)
            
            translations = {
                'metadata': {
                    'source': str(html_path),
                    'version': '1.0',
                    'languages': list(LANGUAGES.keys())
                },
                'content': {}
            }

            for lang_code, lang_info in LANGUAGES.items():
                if lang_code == 'en':
                    translations['content']['en'] = source_content
                    logging.info(f"Using source content for English")
                else:
                    try:
                        translated = self.translate_content(source_content, lang_code)
                        translations['content'][lang_code] = translated
                        logging.info(f"Successfully translated to {lang_info['native']}")
                    except Exception as e:
                        logging.error(f"Failed to translate to {lang_info['native']}: {str(e)}")
                        translations['content'][lang_code] = {
                            'title': f"TRANSLATION_PENDING: {lang_info['native']}",
                            'sections': [],
                            'links': source_content['links']
                        }

            # Ensure all content is YAML-serializable
            def make_yaml_safe(data):
                if isinstance(data, dict):
                    return {k: make_yaml_safe(v) for k, v in data.items()}
                elif isinstance(data, list):
                    return [make_yaml_safe(item) for item in data]
                elif isinstance(data, (str, int, float, bool)):
                    return data
                else:
                    return str(data)

            safe_translations = make_yaml_safe(translations)
            
            # Save YAML
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(
                    safe_translations, 
                    f, 
                    allow_unicode=True, 
                    width=1000, 
                    sort_keys=False,
                    default_flow_style=False
                )

            logging.info(f"Successfully saved translations to {output_path}")
            return True

        except Exception as e:
            logging.error(f"Failed to generate translations: {str(e)}")
            return False

if __name__ == "__main__":
    translator = HTMLTranslator()
    
    html_path = Path("/home/zaya/Documents/Gitrepos/Linktrees/Business/Dev/Zaya/CRM/Documentation/Emails/Psychoanalysis.html")
    output_path = Path("/home/zaya/Documents/Gitrepos/Linktrees/Business/Dev/Zaya/CRM/Documentation/Emails/Psychoanalysis.yaml")
    
    if not html_path.exists():
        logging.error(f"HTML file not found at {html_path}")
        sys.exit(1)
    
    if translator.generate_translations(html_path, output_path):
        logging.info("Translation process completed successfully")
        sys.exit(0)
    else:
        logging.error("Translation process failed")
        sys.exit(1)