import sys
import os
from pathlib import Path


from conversion_pipeline import markdown_to_html_node
from utils.copy_util import clean_public, copy_static_to_public
from md_extrators import extract_title


current_file_path = os.path.realpath(__file__)
root_dir = Path(os.path.dirname(current_file_path)).parent


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_source = ""
    templ_source = ""
    with open(from_path, "r") as source:
        from_source = source.read()
    with open(template_path, "r") as templ:
        templ_source = templ.read()
    html_node = markdown_to_html_node(markdown=from_source)
    html_text = html_node.to_html()
    title = extract_title(markdown=from_source)
    dest_src = templ_source.replace("{{ Title }}", title)
    dest_src = dest_src.replace("{{ Content }}", html_text)
    dest_src = dest_src.replace('href="/', f'href="{basepath}')
    dest_src = dest_src.replace('src="/', f'src="{basepath}')
    if not dest_path.parent.exists():
        os.makedirs(dest_path.parent)
    with open(dest_path, "w") as dest:
        dest.write(dest_src)


def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    contents = os.listdir(dir_path_content)
    for content in contents:
        content_path = dir_path_content.joinpath(content).absolute()
        dest_path = dest_dir_path.joinpath(content).absolute()
        if os.path.isdir(content_path):
            generate_page_recursive(content_path, template_path, dest_path, basepath)
        else:
            generate_page(
                from_path=content_path,
                template_path=template_path,
                dest_path=dest_path.with_suffix(".html"),
                basepath=basepath,
            )


def main():
    basepath = sys.argv[1]
    if not basepath:
        basepath = "/"
    docs_path = root_dir.joinpath("docs")
    static_path = root_dir.joinpath("static")
    clean_public(docs_path)
    copy_static_to_public(c_public_path=docs_path, c_static_path=static_path)
    content_dir_path = root_dir.joinpath("content").absolute()
    templ_path = root_dir.joinpath("template.html").absolute()
    generate_page_recursive(content_dir_path, templ_path, docs_path, basepath)


main()
