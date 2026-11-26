"""Adquisición de la revisión documentada del conjunto Face-Mask-Detection."""
import csv
import hashlib
import io
import json
import os
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

import pyarrow.parquet as pq
from PIL import Image

REVISION = "94f1027682f626d131292f65e36bade192d653f1"
URL = ("https://huggingface.co/datasets/DamarJati/Face-Mask-Detection/"
       f"resolve/{REVISION}/default/train/0000.parquet")
SHA256 = "4e4ef596556332bb0dfbf15eb755859e316eee1e20eec46d49f48762b967b308"
CLASSES = ["WithMask", "WithoutMask"]
FIELDS = ["row_id", "image_path", "label", "class_name", "width_px",
          "height_px", "mode", "image_sha256"]


def checksum(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def acquire(root):
    raw = root / "data" / "raw" / "train.parquet"
    raw.parent.mkdir(parents=True, exist_ok=True)
    if raw.exists() and checksum(raw) == SHA256:
        return raw
    with NamedTemporaryFile(dir=raw.parent, delete=False) as target:
        temporary = Path(target.name)
    try:
        with urlopen(URL, timeout=120) as source, temporary.open("wb") as dest:
            shutil.copyfileobj(source, dest)
        if checksum(temporary) != SHA256:
            raise ValueError("El archivo descargado difiere de la revisión documentada.")
        os.replace(temporary, raw)
    finally:
        temporary.unlink(missing_ok=True)
    return raw


def inventory(raw, output):
    parquet = pq.ParquetFile(raw)
    meta = json.loads(parquet.schema_arrow.metadata[b"huggingface"])
    if meta["info"]["features"]["label"]["names"] != CLASSES:
        raise ValueError("Cambió la codificación de clases.")
    output.mkdir(parents=True, exist_ok=True)
    counts = Counter()
    labels_by_hash = defaultdict(set)
    total = 0
    with NamedTemporaryFile(mode="w", encoding="utf-8", newline="",
                            dir=output, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            writer = csv.writer(stream)
            writer.writerow(FIELDS)
            for batch in parquet.iter_batches(batch_size=64, columns=["image", "label"]):
                for record in batch.to_pylist():
                    label = record["label"]
                    if label not in (0, 1):
                        raise ValueError(f"Etiqueta inválida en fila {total}")
                    image = record["image"]
                    payload = image["bytes"]
                    with Image.open(io.BytesIO(payload)) as photo:
                        photo.load()
                        digest = hashlib.sha256(payload).hexdigest()
                        writer.writerow([total, image["path"], label, CLASSES[label],
                                         photo.width, photo.height, photo.mode, digest])
                    labels_by_hash[digest].add(label)
                    counts[CLASSES[label]] += 1
                    total += 1
            if total != 11792 or len(counts) != 2:
                raise ValueError("Inventario incompleto para esta revisión.")
        except BaseException:
            stream.close()
            temporary.unlink(missing_ok=True)
            raise
    os.replace(temporary, output / "inventory.csv")
    return {"rows": total, "class_counts": dict(counts),
            "distinct_hashes": len(labels_by_hash),
            "duplicate_extra_rows": total - len(labels_by_hash),
            "hashes_with_conflicting_labels": sum(len(x) > 1 for x in labels_by_hash.values()),
            "source_revision": REVISION, "source_sha256": SHA256}
