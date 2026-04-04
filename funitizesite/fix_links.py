import os
import bs4
import re

print("Searching for HTML files to update...")

# Find all the new HTML files we just created
html_files = [f for f in os.listdir('.') if f.endswith('.html') and f.startswith('page-')]

for filename in html_files:
    # Read the file
    with open(filename, 'r', encoding='utf-8') as f:
        soup = bs4.BeautifulSoup(f.read(), 'html.parser')

    links_updated = 0
    # Find every link (<a> tag) on the page
    for a_tag in soup.find_all('a'):
        onclick_attr = a_tag.get('onclick', '')
        
        # If the link uses the old Javascript showPage routing
        if onclick_attr and 'showPage(' in onclick_attr:
            # Extract the page name (e.g., gets "about" from "showPage('about')")
            match = re.search(r"showPage\(['\"]([^'\"]+)['\"]\)", onclick_attr)
            if match:
                page_name = match.group(1)
                
                # Create the standard HTML link to the new file
                a_tag['href'] = f"page-{page_name}.html"
                
                # Delete the old Javascript onclick attribute
                del a_tag['onclick']
                
                links_updated += 1

    # Save the updated file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print(f"✅ Fixed {links_updated} links in {filename}")

print("All navigation links updated successfully!")