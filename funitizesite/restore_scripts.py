import os
import bs4

# Your master file name
original_filename = 'Funitize_linkable_working_test.html'

print("Extracting JavaScript from the original file...")

# 1. Open the original file and find all the scripts in the body
with open(original_filename, 'r', encoding='utf-8') as f:
    soup = bs4.BeautifulSoup(f.read(), 'html.parser')

scripts_to_restore = ""
if soup.body:
    # Grab every <script> tag found inside the body
    for script in soup.body.find_all('script'):
        scripts_to_restore += str(script) + "\n"

print("Injecting scripts into the new pages...")

# 2. Find all your newly created pages
html_files = [f for f in os.listdir('.') if f.endswith('.html') and f.startswith('page-')]

for filename in html_files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 3. Inject the scripts right before the closing </body> tag
    if '</body>' in content:
        # Check to make sure we don't accidentally do it twice
        if '' not in content:
            injection = f"\n\n{scripts_to_restore}\n</body>"
            content = content.replace('</body>', injection)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Restored JavaScript to {filename}")
        else:
            print(f"⏩ Scripts already restored in {filename}")

print("All done! Your animations and effects should be working now.")
