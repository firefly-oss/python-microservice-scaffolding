# scripts/combine_openapi.py

# =======================================================================
# ⚙️ 1. IMPORTS
# =======================================================================
import subprocess
import os
import glob
import yaml
import copy
import argparse
import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

BASE_OPENAPI_PATH = "src/static/base_template.yaml"
FINAL_OPENAPI_PATH = "src/static/opeanpi.yaml"


# =======================================================================
# 📦 2. GLOBAL CONFIGURATIONS & CONSTANTS
# =======================================================================

# Default AWS API Gateway integration settings for CORS preflight (OPTIONS) requests.
# This mock integration ensures that browsers receive the necessary headers.
CORS_AMAZON_APIGATEWAY_INTEGRATION = {
    "summary": "CORS support",
    "description": "Enable CORS by returning correct headers",
    "tags": ["CORS"],
    "responses": {
        "200": {
            "description": "Default response for CORS method",
            "headers": {
                "Access-Control-Allow-Origin": {"schema": {"type": "string"}},
                "Access-Control-Allow-Methods": {"schema": {"type": "string"}},
                "Access-Control-Allow-Headers": {"schema": {"type": "string"}},
            },
            "content": {"application/json": {"schema": {"type": "object"}}},
        }
    },
    "x-amazon-apigateway-integration": {
        "type": "mock",
        "requestTemplates": {"application/json": '{"statusCode": 200}'},
        "passthroughBehavior": "never",
        "responses": {
            "default": {
                "statusCode": "200",
                "responseParameters": {
                    "method.response.header.Access-Control-Allow-Headers": "'*'",
                    "method.response.header.Access-Control-Allow-Methods": "'*'",
                    "method.response.header.Access-Control-Allow-Origin": "'*'",
                },
                "responseTemplates": {"application/json": "{}"},
            }
        },
    },
}

# Default AWS API Gateway integration settings for standard backend methods.
# This configures the endpoint to act as a proxy to the main Lambda handler.
DEFAULT_INTEGRATION = {
    "x-amazon-apigateway-integration": {
        "httpMethod": "POST",
        "passthroughBehavior": "when_no_match",
        "type": "aws_proxy",
        "uri": "MainApiHandler",  # Placeholder for the Lambda function URI.
    },
    "x-amazon-apigateway-request-validator": "all",
    "security": [{"API_KEY": []}],
}


# =======================================================================
# 헬 3. HELPER FUNCTIONS
# =======================================================================


def find_individual_paths_files(services_base_path: str) -> list:
    """
    Scans service directories to find individual OpenAPI path files.
    """
    individual_paths_files = []
    for service_dir in glob.glob(os.path.join(services_base_path, "*/")):
        service_name = os.path.basename(os.path.dirname(service_dir))
        service_openapi_file = os.path.join(service_dir, "openapi", f"{service_name}.yml")
        if os.path.isfile(service_openapi_file):
            individual_paths_files.append(service_openapi_file)
    return individual_paths_files


def combine_openapi_files(base_path: str, output_path: str, individual_paths_files: list):
    """
    Uses Redocly CLI to join multiple OpenAPI files into one.
    """
    try:
        all_files = [base_path] + individual_paths_files
        command = [
            "npx",
            "--yes",  # Auto-accept install prompt
            "@redocly/cli",
            "join",
            *all_files,
            "-o",
            output_path,
            "--without-x-tag-groups",
        ]

        print(f"Running {command=}")

        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully combined OpenAPI files into: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error combining OpenAPI files: {e}\n{e.stderr}")
        raise


def clean_tags(output_path: str):
    """
    Removes the '_other' suffix that Redocly may add to tags.
    """
    with open(output_path, "r") as file:
        openapi_data = yaml.safe_load(file)

    for _, methods in openapi_data.get("paths", {}).items():
        for _, config in methods.items():
            if "tags" in config:
                config["tags"] = [tag.replace("_other", "") for tag in config["tags"]]

    # Clear the top-level tags list as it's not needed after path-level assignment.
    openapi_data["tags"] = []

    with open(output_path, "w") as file:
        yaml.safe_dump(openapi_data, file, default_flow_style=False, sort_keys=False)


def save_test_definition(input_path: str, output_path: str):
    """
    Creates a version of the OpenAPI spec specifically for testing.
    """
    with open(input_path, "r") as file:
        openapi_data = yaml.safe_load(file)

    # Set a specific OpenAPI version compatible with test parsers.
    openapi_data["openapi"] = "3.1.0"

    with open(output_path, "w") as file:
        yaml.safe_dump(openapi_data, file)
    print(f"Saved test-specific OpenAPI definition to: {output_path}")


def save_docs_definition(input_path: str, output_path: str):
    """
    Creates a version of the OpenAPI spec specifically for documentation.
    """
    with open(input_path, "r") as file:
        openapi_data = yaml.safe_load(file)

    # Add any custom modifications for documentation here.

    with open(output_path, "w") as file:
        yaml.safe_dump(openapi_data, file)
    print(f"Saved documentation-specific OpenAPI definition to: {output_path}")


# =======================================================================
# 🚀 4. MAIN EXECUTION
# =======================================================================


def main():
    """
    Main function to orchestrate the entire OpenAPI combination process.
    """
    # Define file paths.
    base_template_path = BASE_OPENAPI_PATH
    final_api_gateway_path = FINAL_OPENAPI_PATH
    tests_output_path = "tests/test_openapi.yaml"
    docs_output_path = "docs/docs_openapi.yaml"
    services_base_path = "src/services/"

    # --- Main Workflow ---
    individual_files = find_individual_paths_files(services_base_path)
    combine_openapi_files(base_template_path, final_api_gateway_path, individual_files)
    clean_tags(final_api_gateway_path)
    save_docs_definition(final_api_gateway_path, docs_output_path)
    save_test_definition(final_api_gateway_path, tests_output_path)

    print("\n✅ OpenAPI specification processing complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine and configure OpenAPI files for AWS API Gateway.")

    args = parser.parse_args()
    main()
