# **Terraform GCP Documentation Agent for Amazon Q**

This project contains the configuration for a custom Amazon Q agent designed to automate the creation of documentation for Terraform code that manages Google Cloud Platform (GCP) resources.

## **Overview**

The agent is composed of two sub-agents:

1. **Terraform Parser**: This agent inspects your Terraform files (\*.tf, \*.tfvars), communicates with configured MCP servers (Terraform, Spacectl, GitHub) to gather contextual information about resources and modules, and creates a local index of this information in JSON format.  
2. **Documentation Generator**: This agent reads the local index files and generates a comprehensive DOCUMENTATION.md file, including an architecture diagram, resource breakdowns, dependencies, and more.

## **Setup**

1. **Install Amazon Q CLI**: Ensure you have the [Amazon Q CLI](https://www.google.com/search?q=https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-cli-installing.html) installed and configured on your system.  
2. **Place Files**: Place the following files into the root directory of your Terraform project:  
   * `.amazonq/cli-agents/terraform-gcp-docs.json` (You may need to create the directories).  
   * `scripts/terraform_parser.sh`  
   * `scripts/documentation_generator.py`  
3. **Make Scripts Executable**: Run the following command in your terminal to make the scripts executable:  
   `chmod +x scripts/terraform_parser.sh`
   `chmod +x scripts/documentation_generator.py`

## **Usage**

1. **Navigate to your Terraform Project**: Open your terminal and change the directory to the root of your Terraform project.  
2. **Start the Agent**: Run the following command to start a chat session with your custom agent.  
   `q chat --agent terraform-gcp-docs`

3. **Run the Terraform Parser**: 
Inside the q chat session, instruct the agent to run the parser script.

`./scripts/terraform_parser.sh`

This will create an index of your resources in the `.q-docs-agent/index/` directory.  

4. **Run the Documentation Generator**: 
Once the parser is finished, instruct the agent to generate the documentation.  
`./scripts/documentation\_generator.py`

This will generate a `DOCUMENTATION.md` file in your project's root directory.
