#!/usr/bin/env python3
"""
Simple direct converter for Jupyter notebooks to hide cells with hideCode:true metadata.
No template or config files needed - just run this script.

Usage:
    python direct_converter.py your_notebook.ipynb
"""

import os
import sys
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import Preprocessor

class HideCodePreprocessor(Preprocessor):
    """Preprocessor to hide code cells with hideCode:true metadata"""
    def preprocess_cell(self, cell, resources, cell_index):
        if cell.cell_type == 'code' and cell.metadata.get('hideCode', False):
            cell.source = ''
            cell.metadata['transient'] = {'remove_source': True}
        return cell, resources

def hide_code_notebook(input_file, output_file=None):
    """Convert notebook with hidden code cells to HTML"""
    print(f"Processing: {input_file}")
    
    # Define output file if not specified
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.html'
    
    # Read the notebook
    with open(input_file, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    # Configure the exporter with custom preprocessor
    exporter = HTMLExporter()
    exporter.register_preprocessor(HideCodePreprocessor(), enabled=True)
    
    # Add custom CSS to hide code cells in the output
    exporter.template_data = {
        'metadata': {
            'html_header': """
<style>
/* CSS to ensure cells with hideCode are hidden */
.jp-InputArea-hidden { 
    display: none !important; 
}
</style>
            """
        }
    }

    # Convert the notebook
    (body, resources) = exporter.from_notebook_node(notebook)
    
    # Add additional CSS directly to the HTML
    hide_code_css = """
<style>
/* Additional CSS to hide input cells */
.jp-InputArea[style*="display: none"],
.jp-InputPrompt[style*="display: none"],
.jp-InputArea-editor[style*="display: none"] {
    display: none !important;
}
</style>
"""
    body = body.replace('</head>', hide_code_css + '</head>')

    # Write the HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(body)
    
    print(f"Conversion complete. HTML saved to: {output_file}")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python direct_converter.py notebook.ipynb [output.html]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
        
    success = hide_code_notebook(input_file, output_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()