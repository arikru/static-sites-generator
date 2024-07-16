import os
import shutil
from generate import copy_contents, generate_pages_recursive

def delete_contents(directory):
    # Ensure the directory exists
    if os.path.exists(directory):
        # Iterate over the items in the directory
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            # Check if the item is a directory or file
            if os.path.isdir(item_path):
                # If it's a directory, delete it and all its contents
                shutil.rmtree(item_path)
            else:
                # If it's a file, delete it
                os.remove(item_path)
        print(f"All contents of the directory '{directory}' have been deleted.")
    else:
        print(f"The directory '{directory}' does not exist.")

def main():
    delete_contents("public")
    copy_contents()
    generate_pages_recursive("content", "template.html", "public")

main()
