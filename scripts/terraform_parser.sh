#!/bin/bash

# Sub-agent Script: Terraform Parser
# This script parses Terraform files, queries MCP servers for context,
# and creates a local index for the documentation generator.

echo "--- Starting Terraform Parser Sub-agent ---"

# Create a directory for index files
INDEX_DIR=".q-docs-agent/index"
mkdir -p "$INDEX_DIR"
echo "Created index directory at $INDEX_DIR"

# 1. Parse all *.tf files for resources and modules
echo "Parsing *.tf files..."
for tf_file in $(find . -name "*.tf"); do
  # Find provider resources (e.g., google_compute_instance)
  grep -E '^\s*resource\s+"([a-zA-Z0-9_-]+)"\s+"([a-zA-Z0-9_-]+)"' "$tf_file" | while read -r line; do
    resource_type=$(echo "$line" | sed -E 's/^\s*resource\s+"([a-zA-Z0-9_-]+)".*/\1/')
    resource_name=$(echo "$line" | sed -E 's/^\s*resource\s+"[a-zA-Z0-9_-]+"\s+"([a-zA-Z0-9_-]+)".*/\1/')
    echo "Found resource: $resource_type '$resource_name'"
    # In a real implementation, you would call the Terraform MCP server here to get context
    # and save it as a JSON file.
    # Example placeholder:
    echo "{\"type\": \"$resource_type\", \"name\": \"$resource_name\", \"provider\": \"gcp\", \"description\": \"Context from Terraform MCP\"}" > "$INDEX_DIR/${resource_name}.json"
  done

  # Find modules from private registry
  grep -E '^\s*module\s+"([a-zA-Z0-9_-]+)"' "$tf_file" | while read -r line; do
    module_name=$(echo "$line" | sed -E 's/^\s*module\s+"([a-zA-Z0-9_-]+)".*/\1/')
    # Assuming the source points to a private registry identifiable by a specific URL pattern
    module_source=$(grep -A 2 "module \"$module_name\"" "$tf_file" | grep 'source\s*=' | cut -d'=' -f2 | tr -d ' "')
    
    if [[ $module_source == *"app.spacelift.io"* ]]; then
        echo "Found Spacelift module: '$module_name' from $module_source"
        # In a real implementation, you would call the Spacectl MCP server here.
        # Example placeholder:
        echo "{\"type\": \"module\", \"name\": \"$module_name\", \"source\": \"$module_source\", \"description\": \"Context from Spacectl MCP\"}" > "$INDEX_DIR/${module_name}.json"
    elif [[ $module_source == *"github.com"* ]]; then
        echo "Found GitHub module: '$module_name' from $module_source"
        # In a real implementation, you would call the GitHub MCP server here.
        # Example placeholder:
        echo "{\"type\": \"module\", \"name\": \"$module_name\", \"source\": \"$module_source\", \"description\": \"Context from GitHub MCP\"}" > "$INDEX_DIR/${module_name}.json"
    fi
  done
done

# 2. Read tfvars files to understand input variables
echo "Parsing *.tfvars files..."
for tfvars_file in $(find . -name "*.tfvars"); do
  echo "Found tfvars file: $tfvars_file"
  # In a real implementation, you would parse this file and store its contents.
  # Example placeholder:
  cp "$tfvars_file" "$INDEX_DIR/input_variables.tfvars"
done

echo "--- Terraform Parser Sub-agent Finished ---"
echo "Local index files have been created successfully."
