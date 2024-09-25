# Static Site Generator

## Overview

Static Site Generator (SSG) is a Python-based tool designed to simplify the creation of static websites. By taking a set of Markdown files as input, SSG converts them into fully-functional HTML files, ready to be served on the web. This tool is perfect for developers, bloggers, and content creators who prefer writing in Markdown but need a streamlined process to generate static web pages.

## Features

- **Markdown to HTML Conversion**: Automatically converts Markdown files (.md) into HTML files.
- **Template Support**: Incorporate HTML templates to maintain a consistent look and feel across all pages.
- **Customization**: Easily customize the output HTML with CSS and JavaScript.
- **Fast and Lightweight**: Efficiently processes files with minimal overhead.
- **Easy to Use**: Simple command-line interface for quick setup and generation.

## Getting Started

1. **Installation**: Fork and clone the repository.
   ```bash
   git clone https://github.com/yourusername/static-sites-generator.git
   cd static-sites-generator
   ```

2. **Usage**: Simply run the main.sh script with your Markdown files in the `content` folder.
   ```bash
   ./main.sh
   ```

3. **Serve**: Use any web server to serve the generated HTML files (running the main script automatically starts a local server defined in `server.py` that previews the created HTML files).
