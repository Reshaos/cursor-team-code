#!/usr/bin/env python3
"""Build a reproducible source ZIP after validation. No network or provider APIs."""
import hashlib
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
from validate import ROOT, validate


def package(root=ROOT, output=None):
    root = Path(root)
    failures = validate(root)
    if failures:
        raise ValueError("; ".join(failures))
    import json
    version = json.loads((root / "plugins/team-code/.cursor-plugin/plugin.json").read_text())["version"]
    output = Path(output) if output else root / "dist" / f"cursor-team-code-{version}.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    excluded = {".git", "dist", "__pycache__", ".work"}
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root)
            if not path.is_file() or any(x in excluded for x in relative.parts) or path.suffix == ".pyc" or path.resolve() == output.resolve():
                continue
            info = ZipInfo("cursor-team-source/" + relative.as_posix(), (2020, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(".sha256").write_text(f"{digest}  {output.name}\n", encoding="utf-8")
    return output, digest


if __name__ == "__main__":
    archive, digest = package()
    print(archive)
    print("SHA256:", digest)
