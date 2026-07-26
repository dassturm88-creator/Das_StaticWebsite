from markdown import markdown_to_html_node
import os

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            title = line.lstrip("#").strip()
            return title
    raise Exception("no h1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown_content = f.read()
    with open(template_path) as f:
        template_content = f.read()
    node = markdown_to_html_node(markdown_content)
    html_string = node.to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_string)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        base, _ = os.path.splitext(filename)
        filename_html = base + ".html"
        file_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename_html)
        dest_path_dir = os.path.join(dest_dir_path, filename)
        if os.path.isfile(file_path):
            generate_page(file_path, template_path, dest_path)
        else:
            generate_pages_recursive(file_path, template_path, dest_path_dir)