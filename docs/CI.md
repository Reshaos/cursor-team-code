# Provider-neutral CI packaging contract
Use an existing organizational Python 3.10+ runner. No service connection, cloud credential or external package is required by these scripts. A pipeline wrapper for Azure DevOps, GitHub or another provider should call the same commands, fail on any nonzero exit, and collect `dist/*.zip` plus `dist/*.sha256` as private artifacts:

```text
python3 scripts/validate.py
python3 scripts/test_package.py
python3 scripts/package.py
```

On Windows use your existing `py -3` launcher if appropriate. Configure that wrapper in your private Git process; this package does not publish artifacts, call provider APIs or alter CI/security settings. Artifact upload steps are provider-specific and intentionally left to your existing approved pipeline.

Packaging uses a fixed ZIP timestamp and sorted paths and is reproducible for identical source bytes. Different checkout line endings can change the checksum; preserve the supplied .gitattributes. It excludes dist, Git metadata, caches and local work. The source revision/version should be recorded by your existing pipeline in its own logs. Validation checks package structure, not agent execution or Cursor acceptance. The packaging self-test uses temporary isolated copies, mutation cases, hook JSON fixtures and byte comparison; it invokes no network or application code.
