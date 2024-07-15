import os, shutil

from block import markdown_to_html_node
from extract import extract_title

def copy_contents(src="static", dst="public"):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    src_contents = os.listdir(src)

    for item in src_contents:
        src_path = os.path.join(src,item)
        dst_path = os.path.join(dst,item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_contents(src=src_path, dst=dst_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        src_file = f.read()

    with open(template_path, "r") as f:
        tpl_file = f.read()

    html_string = markdown_to_html_node(src_file).to_html()

    title = extract_title(src_file)

    tpl_file = tpl_file.replace("{{ Title }}", title)
    tpl_file = tpl_file.replace("{{ Content }}", html_string)

    dir_path = os.path.dirname(dest_path)

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    with open(dest_path, "w") as f:
        f.write(tpl_file)

