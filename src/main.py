from markdown import *
import os, shutil


def copy_tree(src, path):
    if not os.path.exists(src):
        raise FileNotFoundError(f"The directory {src} doesn't exits.")

    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

    copy_tree_r(src, path)


def copy_tree_r(src, path):
    dir_list = os.listdir(src)
    for dir in dir_list:
        src_dir = os.path.join(src, dir)

        if os.path.isfile(src_dir):
            shutil.copy(src_dir, path)

        if os.path.isdir(src_dir):
            path_dir = os.path.join(path, dir)
            os.mkdir(path_dir)
            copy_tree_r(src_dir, path_dir)


def extract_title(markdown):
    m = re.match(r"# (.+)", markdown)
    if not m:
        raise Exception("All pages need a single h1 header.j")
    title = m.group(1)
    return title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(markdown)
    content = markdown_to_htmlnode(markdown).to_html()

    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    with open(dest_path, "w") as f:
        f.write(html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dirs = os.listdir(dir_path_content)
    for dir in dirs:
        dest_path = os.path.join(dest_dir_path, dir)
        src_path = os.path.join(dir_path_content, dir)
        if os.path.isfile(src_path):
            dest_path = dest_path.replace(".md", ".html")
            print(dest_path)
            generate_page(
                src_path,
                template_path,
                dest_path,
            )
        if os.path.isdir(src_path):
            os.mkdir(dest_path)
            generate_pages_recursive(src_path, template_path, dest_path)


copy_tree("static", "public")
generate_pages_recursive("content/", "template.html", "public/")
