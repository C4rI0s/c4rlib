# Releasing c4rlib

Releases are cut by pushing a tag. CI does the rest: it verifies the tag matches
the package version, runs the tests, builds the distributions, uploads to PyPI
via Trusted Publishing, and creates the GitHub release.

## One-time setup

### 1. Register the Trusted Publisher on PyPI

This replaces the API token entirely — GitHub mints a short-lived OIDC token per
run, so there is no long-lived credential to leak.

Go to <https://pypi.org/manage/project/c4rlib/settings/publishing/> and add a
publisher with exactly these values:

| Field             | Value            |
| ----------------- | ---------------- |
| Owner             | `C4rI0s`         |
| Repository name   | `c4rlib`         |
| Workflow filename | `publish.yml`    |
| Environment name  | `pypi`           |

### 2. Create the `pypi` environment on GitHub

`Settings → Environments → New environment → pypi`. Optionally add yourself as a
required reviewer so every release pauses for one click before upload.

### 3. Revoke the old API token

Once a Trusted Publisher works, delete any remaining token at
<https://pypi.org/manage/account/token/>. Nothing needs it anymore.

## Cutting a release

1. Update `CHANGELOG.md`: move `## [Unreleased]` entries under the new version
   heading and add the compare link at the bottom.
2. Bump the version in **both** places — they must agree or CI fails the release:
   - `pyproject.toml` → `version`
   - `c4rlib/__init__.py` → `__version__`
3. Commit, then tag and push:

   ```bash
   git commit -am "Release v3.1.0"
   git tag v3.1.0
   git push origin main --tags
   ```

4. Watch the run at `Actions → Publish to PyPI`. If the `pypi` environment has a
   required reviewer, approve it there.
5. Verify: `pip install --upgrade c4rlib` and check `c4rlib.__version__`.

PyPI never allows re-uploading a version. If a release is broken, bump the patch
version and release again — there is no overwriting.

## Testing a release without publishing

```bash
python -m build
twine check --strict dist/*
pip install --force-reinstall dist/c4rlib-*.whl
cd /tmp && python -c "import c4rlib; print(c4rlib.__version__)"
```

That last `cd` matters: the package lives at the repo root, so importing from
inside the checkout picks up the source tree rather than the installed wheel.

To rehearse the full upload against TestPyPI, add a second Trusted Publisher at
<https://test.pypi.org> and run the publish workflow manually with
`workflow_dispatch`.

## Regenerating the README demos

The GIFs are produced from the `.tape` scripts in `demos/`, so they stay in sync
with the real API. Requires [vhs](https://github.com/charmbracelet/vhs):

```bash
winget install charmbracelet.vhs     # Windows
brew install vhs                     # macOS

cd demos
vhs intro.tape        # writes ../assets/intro.gif
```

See [demos/README.md](../demos/README.md) for the full list.
