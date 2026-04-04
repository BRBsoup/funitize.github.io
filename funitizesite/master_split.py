import bs4
import re

# Your master file
original_filename = 'Funitize_linkable_working_test.html'

print(f"Reading original file: {original_filename}...")
with open(original_filename, 'r', encoding='utf-8') as f:
    original_html = f.read()

# Find out what pages we need to create
temp_soup = bs4.BeautifulSoup(original_html, 'html.parser')
page_sections = temp_soup.find_all('div', class_='page-section')
page_ids = [section.get('id') for section in page_sections if section.get('id')]

print(f"Found {len(page_ids)} pages to generate: {', '.join(page_ids)}")

for target_id in page_ids:
    # 1. Start with a fresh, COMPLETE copy of the original file for EVERY page
    soup = bs4.BeautifulSoup(original_html, 'html.parser')
    
    # 2. Delete all other page sections except the target one
    for section in soup.find_all('div', class_='page-section'):
        if section.get('id') != target_id:
            section.decompose() # This safely removes the HTML element
            
    # 3. Force the target section to be visible (overriding the old hiding logic)
    target_section = soup.find('div', id=target_id)
    if target_section:
        target_section['style'] = target_section.get('style', '') + '; display: block !important; opacity: 1 !important; visibility: visible !important;'
        
    # 4. Fix the navigation links automatically
    for a_tag in soup.find_all('a'):
        # Fix standard hash links (e.g., href="#page-about")
        href = a_tag.get('href', '')
        if href.startswith('#page-'):
            a_tag['href'] = href.replace('#', '') + '.html'
            
        # Fix Javascript routing links (e.g., onclick="showPage('about')")
        onclick = a_tag.get('onclick', '')
        if 'showPage(' in onclick:
            match = re.search(r"showPage\(['\"]([^'\"]+)['\"]\)", onclick)
            if match:
                page_name = match.group(1)
                # Ensure the filename format is correct
                if not page_name.startswith('page-'):
                    page_name = 'page-' + page_name
                    
                a_tag['href'] = f"{page_name}.html"
                del a_tag['onclick'] # Remove the old javascript click event

    # 5. Save the perfectly constructed page
    filename = f"{target_id}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print(f"✅ Created {filename} (Includes ALL original scripts and styles)")

print("\nSuccess! All pages regenerated flawlessly.")
