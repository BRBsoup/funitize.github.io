import bs4
import os

# Define the input filename
input_filename = 'Funitize_linkable_working_test.html'

print(f"Reading {input_filename}...")

# 1. Read the local HTML file
with open(input_filename, 'r', encoding='utf-8') as file:
    html_content = file.read()

# 2. Parse the HTML content
soup = bs4.BeautifulSoup(html_content, 'html.parser')

# Extract common sections
head = soup.head
nav = soup.nav
footer = soup.footer

# Find all page sections
page_sections = soup.find_all('div', class_='page-section')

# 3. Create a new HTML file for each page section
for page_section in page_sections:
    # Get the ID of the page section to use as the filename
    page_id = page_section.get('id')
    if page_id:
        # Create a new BeautifulSoup object for the new page
        new_soup = bs4.BeautifulSoup('<!DOCTYPE html><html lang="en"></html>', 'html.parser')
        html_tag = new_soup.html
        
        # Append the common head, nav, the specific page section, and the common footer
        if head: html_tag.append(head)
        
        body_tag = new_soup.new_tag('body')
        html_tag.append(body_tag)
        
        if nav: body_tag.append(nav)
        body_tag.append(page_section)
        if footer: body_tag.append(footer)
        
        # Save the new page to a file
        filename = f"{page_id}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(new_soup))
            print(f"✅ Created {filename}")

print("Finished splitting the website!")