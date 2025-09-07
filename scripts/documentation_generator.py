#!/usr/bin/env python3

import os
import json
import glob

# Sub-agent Script: Documentation Generator
# This script reads the index files created by the parser and generates
# a final DOCUMENTATION.md file.

INDEX_DIR = ".q-docs-agent/index"
OUTPUT_FILE = "DOCUMENTATION.md"

def generate_header():
    """Generates the main header for the documentation."""
    return "# Terraform GCP Infrastructure Documentation\n\n"

def generate_architecture_diagram():
    """Generates a placeholder for the architecture diagram."""
    # In a real implementation, this could use a tool like graphviz
    # to generate a diagram based on resource dependencies.
    content = "## High-Level Architecture\n\n"
    content += "\n\n"
    content += "This diagram illustrates the relationships between the major GCP resources managed by this Terraform configuration.\n\n"
    return content

def generate_resource_breakdown():
    """Generates the resource breakdown section from JSON index files."""
    content = "## Resource Breakdown\n\n"
    content += "| GCP Service | Resource Name | Key Configurations |\n"
    content += "|-------------|---------------|--------------------|\n"
    
    for file_path in glob.glob(os.path.join(INDEX_DIR, '*.json')):
        if "module" in file_path:
            continue
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                if data.get("type") != "module":
                    service = data.get("type", "N/A").replace("google_", "").replace("_", " ").title()
                    name = data.get("name", "N/A")
                    description = data.get("description", "No details available.")
                    content += f"| {service} | `{name}` | {description} |\n"
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {file_path}")
    
    content += "\n"
    return content

def generate_module_breakdown():
    """Generates the module breakdown section."""
    content = "## Module Breakdown\n\n"
    content += "| Module Name | Source | Description |\n"
    content += "|-------------|--------|-------------|\n"

    for file_path in glob.glob(os.path.join(INDEX_DIR, '*.json')):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                if data.get("type") == "module":
                    name = data.get("name", "N/A")
                    source = data.get("source", "N/A")
                    description = data.get("description", "No details available.")
                    content += f"| `{name}` | `{source}` | {description} |\n"
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {file_path}")

    content += "\n"
    return content

def generate_input_variables():
    """Generates the input variables section from the tfvars file."""
    content = "## Input Variables (`.tfvars`)\n\n"
    tfvars_path = os.path.join(INDEX_DIR, 'input_variables.tfvars')
    if os.path.exists(tfvars_path):
        with open(tfvars_path, 'r') as f:
            content += "```hcl\n"
            content += f.read()
            content += "\n```\n"
    else:
        content += "No `.tfvars` file was found or indexed.\n"
    
    content += "\n"
    return content

def main():
    """Main function to generate the documentation."""
    print("--- Starting Documentation Generator Sub-agent ---")
    if not os.path.exists(INDEX_DIR):
        print(f"Error: Index directory '{INDEX_DIR}' not found. Please run the parser first.")
        return

    with open(OUTPUT_FILE, 'w') as doc_file:
        doc_file.write(generate_header())
        doc_file.write(generate_architecture_diagram())
        doc_file.write(generate_resource_breakdown())
        doc_file.write(generate_module_breakdown())
        doc_file.write(generate_input_variables())
        # Placeholder for Dependencies and Outputs sections
        doc_file.write("## Dependencies\n\n(Dependency analysis to be implemented)\n\n")
        doc_file.write("## Outputs\n\n(Output analysis to be implemented)\n\n")

    print(f"--- Documentation Generator Sub-agent Finished ---")
    print(f"Documentation successfully generated at {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
