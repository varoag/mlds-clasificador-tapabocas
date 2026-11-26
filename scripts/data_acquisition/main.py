"""Ejecutar desde cualquier carpeta después de instalar el proyecto."""
import json
from pathlib import Path

from tapabocas.database.acquisition import acquire, inventory


def main():
    root = Path(__file__).resolve().parents[2]
    result = inventory(acquire(root), root / "data" / "interim")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
