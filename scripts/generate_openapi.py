import sys
from pathlib import Path

# Add the project root to the sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import yaml

from src.core.fastapi.api_handler import app


def generate_openapi_yaml():
    openapi_schema = app.openapi()
    openapi_schema["openapi"] = "3.0.3"
    openapi_yaml = yaml.dump(openapi_schema, sort_keys=False, default_flow_style=False)

    output_path = Path("docs/openapi.yaml")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(openapi_yaml)
    print(f"OpenAPI YAML generated and saved to {output_path}")


if __name__ == "__main__":
    generate_openapi_yaml()
