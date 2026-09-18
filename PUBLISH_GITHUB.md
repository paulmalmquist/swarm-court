# Publish this release to GitHub

**Target:** `paulmalmquist/swarm-court`, a **new public** repository.

No repository was created or pushed from the preparation environment. Its GitHub connection exposed only read actions, and its terminal could not resolve GitHub. The script below performs publication on a machine with network access.

## Run

Install Git and the official [GitHub CLI](https://cli.github.com/) if they are not already available. Python 3.11+ is also required by the application.

Extract this archive and, from the `swarm-court` directory, run:

```bash
python scripts/publish_github.py
```

When authentication is needed, the script opens GitHub CLI's browser/device login. Sign in as **paulmalmquist**. Do not paste personal access tokens, passwords or recovery codes into chat.

The script verifies the release hashes, runs the unit tests, stages only the original release files, creates the public repository, pushes `main`, and checks the public visibility and remote commit. It refuses an existing repository, an existing local `.git` directory, a different account, or a modified release file. It does not alter another repository or publish a hosted application. No license is added on your behalf.

If a network failure occurs after repository creation, a new empty repository may remain; inspect the terminal message before retrying. The script deliberately will not overwrite it.

## Offline validation

```bash
python scripts/publish_github.py --check
python scripts/api_check.py
```

Preparation checks passed: 23 core unit tests and 12 local HTTP checks. The existing UI results are from the earlier prototype validation, not a new browser-to-server run. The optional semantic adapter and work Claude execution remain unvalidated against real work systems.

A credential-pattern scan found no matches in the release text. This is not a comprehensive security audit. Connections remain unconfigured, examples remain synthetic, and model execution remains disabled. Runtime databases, environment files, private keys and local caches are excluded. Keep this public seed separate from any later private work integration.
