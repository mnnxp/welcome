#!/usr/bin/env python3
import os
import json
import shutil
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, StrictUndefined

total_generated = 0

def load_translations(lang_code):
    """Load translations for the specified language"""
    try:
        with open(f'i18n/locales/{lang_code}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Translations for {lang_code} not found")
        return None

def setup_jinja_environment():
    """Set up Jinja2 environment"""
    return Environment(
        loader=FileSystemLoader(['.', 'i18n/templates']),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False
    )

def smart_url(url, base_url, page_name):
    """Apply base_url only for relative paths"""
    if (url.startswith('#') and page_name == 'index') or url.startswith('mailto:'):
        return f'href=\"{url}\"'
    if url.startswith('http://') or url.startswith('https://'):
        return f'href=\"{url}\" target=\"_blank\" rel=\"noopener noreferrer\"'
    if url.startswith('/'):
        return f'href=\"{base_url.rstrip('/') + url}\"'
    return f'href=\"{base_url.rstrip('/') + '/' + url}\"'

def render_page(env, page_variables, template_path, output_path):
    """Render template with provided variables and save result to specified path"""
    global total_generated

    # Render template
    template = env.get_template(template_path)
    rendered_content = template.render(**page_variables)

    # Save result
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered_content)

    print(f"Created: {output_path}")
    total_generated += 1

def generate_with_env(env, lang, base_variables, pages, output_dir):
    """Generate page set for specified language using Jinja2 environment and base variables."""
    for page_info in pages:
        page_name = page_info['name']
        assets_prefix = page_info['assets_prefix']
        template_path = page_info['template']
        relative_path = page_info['relative']
        output_path = f'{output_dir}/{lang}/{relative_path}'
        # Create directory for output file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        try:
            # Set page name for template
            page_variables = base_variables.copy()
            page_variables['page_name'] = page_name
            page_variables['assets_prefix'] = assets_prefix
            render_page(
                env,
                page_variables,
                template_path,
                output_path
                )
        except TemplateNotFound:
            print(f"Template not found: {template_path}")
        except Exception as e:
            print(f"Error generating {output_path}: {e}")

def generate_articles_from_json(env, lang, base_variables, json_articles, template_path, output_dir):
    """Generate page set from JSON (overviews.articles) using Jinja2 environment and base variables."""
    global total_generated

    # Load JSON
    with open(json_articles, 'r', encoding='utf-8') as f:
        data = json.load(f)

    template = env.get_template(template_path)
    articles = data.get('overviews', {}).get('articles', [])

    for article in articles:
        # Skip external articles
        if article.get('external', False):
            continue

        # Create path for article
        page_name = article['page_name']
        article_dir = os.path.join(output_dir, page_name)
        os.makedirs(article_dir, exist_ok=True)

        output_path = os.path.join(article_dir, 'index.html')

        try:
            # Prepare variables
            page_variables = base_variables.copy()
            page_variables['art'] = article
            page_variables['page_name'] = page_name
            page_variables['assets_prefix'] = '../../../'
            render_page(
                env,
                page_variables,
                template_path,
                output_path
                )
        except TemplateNotFound:
            print(f"Template not found: {template_path}")
        except Exception as e:
            print(f"Error generating from json {output_path}: {e}")

def generate_pages():
    """Generate static pages"""

    global total_generated

    languages = ['en', 'ru', 'zh']
    # Templates and location of created files
    tml = [
        # ('index',''),
        ('overviews',''),
        ('privacy-notice',''),
        ('terms','')
        ]
    pages = [{
            'name': 'index',
            'template': f'pages/index/template.html',
            'base_template': 'i18n/templates/base.html',
            'relative': f'index.html',
            'assets_prefix': '../'
            }]
    for (t,r) in tml:
        pages.append({
            'name': t,
            'template': f'pages/{t}/template.html',
            'base_template': 'i18n/templates/base.html',
            'relative': f'{r}{t}/index.html',
            'assets_prefix': '../../'
            })
    env = setup_jinja_environment()
    # Register url processing in environment
    env.filters['smart_url'] = smart_url
    total_generated = 0

    # Create output directory
    output_dir = 'dist'
    os.makedirs(output_dir, exist_ok=True)

    print(f"🌐 Generation")
    for lang in languages:
        print(f"For language: {lang}")

        # Load translations
        translations = load_translations(lang)
        if not translations:
            continue

        # Base variables for all templates
        base_variables = {
            'lang_code': lang,
            'page_name': '',  # Will be set for each page
            **translations
        }

        generate_with_env(env, lang, base_variables, pages, output_dir)

        generate_articles_from_json(
            env,
            lang,
            base_variables,
            json_articles=f'i18n/locales/{lang}.json',
            template_path='pages/overviews/article/template.html',
            output_dir=f'dist/{lang}/overviews'
        )

    print(f"Generation completed! Pages created: {total_generated}")
    print(f"Files saved to directory: {output_dir}/")

def create_sample_structure():
    """Create sample file structure (for testing)"""
    print("Creating sample files...")

    # Create directories
    os.makedirs('i18n/locales', exist_ok=True)
    os.makedirs('i18n/templates', exist_ok=True)
    os.makedirs('pages/index', exist_ok=True)
    os.makedirs('pages/overviews', exist_ok=True)

    print("Structure created. Run the script again to generate pages.")

if __name__ == "__main__":
    print("CADBase Multilingual Site Generator")
    print("=" * 50)

    # Check if required files exist
    if not os.path.exists('i18n/locales/en.json'):
        create_sample_structure()
    else:
        generate_pages()