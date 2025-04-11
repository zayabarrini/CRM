#!/usr/bin/env python3
import sys
import re
from pathlib import Path
from translationFunctions import translate_text

# Supported languages (ISO 639-1 codes)
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'ru': 'Russian',
    'zh-ch': 'Chinese (Simplified)',
    'jp': 'Japanese',
    'hi': 'Hindi',
    'ar': 'Arabic',
    'ko': 'Korean'
}

# Original English template
EN_TEMPLATE = """Subject: Collaboration Opportunity in Psychoanalysis and Digital Art

Dear {name},

I hope this message finds you well. My name is Zaya Barrini, and I work at the intersection of psychoanalysis, cinema, and digital art. As a specialist in Lacanian psychoanalysis, I've developed courses, clinical programs, and creative projects that bridge theoretical frameworks with artistic expression.

I'm currently seeking meaningful collaborations with institutions and professionals engaged in:
- Psychoanalytic theory and practice
- Clinical supervision and research
- Experimental digital art projects

You can explore my work, including an ongoing project on the topology of the Klein Bottle and its psychoanalytic applications, at: zayabarrini.vercel.app

I would welcome the opportunity to discuss potential collaborations, which could include:
✓ Guest lectures or course development
✓ Clinical supervision partnerships
✓ Joint research initiatives
✓ Interdisciplinary art projects

Would you be available for a conversation in the coming weeks? I'm happy to accommodate your schedule.

Looking forward to your thoughts.

Best regards,
Zaya Barrini"""

def translate_template(template, target_lang):
    """Translate template while preserving placeholders and formatting"""
    # Split into lines for better translation handling
    lines = template.split('\n')
    translated_lines = []
    
    for line in lines:
        if line.strip().startswith('Subject:'):
            # Translate subject separately
            prefix, subject = line.split(':', 1)
            translated_subject = translate_text(subject.strip(), target_lang)
            translated_lines.append(f"{prefix}: {translated_subject}")
        elif line.strip().startswith(('✓', '-')) or ':' in line:
            # Handle lists and special formatting
            parts = line.split(' ', 1)
            if len(parts) > 1:
                translated = translate_text(parts[1], target_lang)
                translated_lines.append(f"{parts[0]} {translated}")
            else:
                translated_lines.append(line)
        else:
            # Regular text
            translated_lines.append(translate_text(line, target_lang))
    
    return '\n'.join(translated_lines)

def generate_template_file(output_path="/home/zaya/Documents/Gitrepos/Linktrees/Business/Dev/Zaya/CRM/Documentation/Emails/Psychoanalysis-ml.md"):
    """Generate multilingual template file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Email Templates by Language\n\n")
        
        for lang_code, lang_name in LANGUAGES.items():
            if lang_code == 'en':
                # Use original English version
                f.write(f"[{lang_code}]\n{EN_TEMPLATE}\n\n")
            else:
                try:
                    translated = translate_template(EN_TEMPLATE, lang_code)
                    f.write(f"[{lang_code}]\n{translated}\n\n")
                    print(f"Generated {lang_name} translation")
                except Exception as e:
                    print(f"Failed to translate to {lang_name}: {str(e)}")
                    # Create placeholder for manual translation
                    f.write(f"[{lang_code}]\n# TODO: MANUAL TRANSLATION NEEDED FOR {lang_name}\n\n")
    
    print(f"\nTemplate file generated at: {Path(output_path).absolute()}")
    print("Please review machine translations before use!")

if __name__ == "__main__":
    generate_template_file()