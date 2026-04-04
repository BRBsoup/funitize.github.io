import os

print("Applying visibility fix to all HTML pages...")

# Find all the new HTML files we created
html_files = [f for f in os.listdir('.') if f.endswith('.html') and f.startswith('page-')]

for filename in html_files:
    # Read the file
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # The CSS we need to inject to force the page section to be visible
    visibility_css = """
<style>
    /* Force the page section to be visible since they are now separate files */
    .page-section {
        display: block !important;
        opacity: 1 !important;
        visibility: visible !important;
        position: relative !important;
        z-index: 10 !important;
    }
</style>
</head>
"""

    # Inject the CSS right before the closing </head> tag
    if '</head>' in content and '/* Force the page section' not in content:
        content = content.replace('</head>', visibility_css)
        
        # Save the updated file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed visibility on {filename}")
    else:
        print(f"⏩ Skipped {filename} (Already fixed or no </head> tag)")

print("All pages should now be visible!")