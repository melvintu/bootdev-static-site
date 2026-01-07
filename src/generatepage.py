import os
from markdown_html import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        from_path_string = f.read()
    with open(template_path, "r") as f:
        template_path_string = f.read()
    node = markdown_to_html_node(from_path_string)
    html = node.to_html()
    title = extract_title(from_path_string)
    html_title= template_path_string.replace("{{ Title }}", title)
    html_content = html_title.replace("{{ Content }}", html)
    html_content = html_content.replace('href="/', f'href="{basepath}')
    html_content = html_content.replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok = True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Page generated from {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(from_path):
            new_filename = filename.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, new_filename)
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            dest_path = os.path.join(dest_dir_path, filename)
            generate_pages_recursive(from_path, template_path, dest_path, basepath)