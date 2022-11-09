import json
from pathlib import Path

from flask import Response

BACKEND_ROOT = Path(".")
RESOURCES_PATH = BACKEND_ROOT / "resources"


def forge_fail_response(reason: str) -> Response:
    return Response(json.dumps({"reason":reason}), content_type="application/json",headers={"success": False})