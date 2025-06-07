import os
import sys
import shutil
from copy_static import copy_directory_recursive
from markdown_blocks import markdown_to_html_node, extract_title

def clear_public_directory(path="public"):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def generate_page(from_path: str, template_path: str, dest_path: str, basepath = "/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

        # Read markdown file
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

        # Read template file
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
 
        # Generate HTML from markdown
    html_node = markdown_to_html_node(markdown)
    content_html = html_node.to_html()

        # Extract title from markdown
    title = extract_title(markdown)

        # Replace placeholders
    result = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    # Replace base path references
    result = result.replace('href="/', f'href="{basepath}')
    result = result.replace('src="/', f'src="{basepath}')

        # Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

        # Write final HTML
    with open(dest_path, "w", encoding="utf-8") as f:
            f.write(result)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    print(f"Generating pages from '{dir_path_content}' to '{dest_dir_path}' using '{template_path}'")

    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                # Full path to the source markdown file
                from_path = os.path.join(root, file)

                # Determine relative path from content root
                rel_path = os.path.relpath(from_path, dir_path_content)

                # Convert .md to .html and build destination path
                dest_rel_path = rel_path.replace(".md", ".html")
                dest_path = os.path.join(dest_dir_path, dest_rel_path)

                # Ensure destination directory exists
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Call your page generation function
                generate_page(from_path, template_path, dest_path, basepath)

   

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    clear_public_directory()
    copy_directory_recursive("static", "docs")
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path="docs",
        basepath=basepath
        )
main()
