# Manage the template with GitHub

## 1. Create your GitHub repository

Create an empty repository in your GitHub account. Do not initialize it with a README because this project already has one. Public repositories allow direct, unauthenticated downloads from your VPS; private repositories require GitHub authentication.

## 2. Commit and push from your Mac

In Terminal:

```sh
cd /Users/circle/Desktop/Projects/m-template
python3 scripts/build.py
git add .
git diff --cached --stat
git commit -m "Prepare CircleWeb template for GitHub"
```

Check whether a remote is already configured:

```sh
git remote -v
```

If there is no `origin`, add your repository URL, replacing `YOUR_USERNAME` and `YOUR_REPO`:

```sh
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

If `origin` already points to the right repository, leave it unchanged. Then push:

```sh
git push -u origin main
```

Use GitHub Desktop, GitHub CLI authentication, or your configured Git credentials if prompted. Do not put tokens in files or remote URLs.

## 3. Make future updates

Edit files in `src/` or replace assets, then rebuild the deployable HTML before committing:

```sh
python3 scripts/build.py
.venv/bin/python -m unittest discover -s tests -v
node --check src/app.js
git add src assets scripts templates tests README.md docs .github requirements-dev.txt
git diff --cached --stat
git commit -m "Update subscription template"
git push
```

Set up `.venv` with the instructions in the README first. GitHub Actions builds and tests each push and pull request, checks that the committed HTML matches the source, and offers a downloadable build artifact. It does not connect to or restart your VPS.

The generated `templates/subscription/index.html` is intentionally tracked for direct VPS downloads. `preview/`, `dist/`, ZIP packages, virtual environments, caches, `.env` files, keys, and backups are ignored. Previously tracked previews and ZIPs are removed from the Git index while remaining on your Mac. This removal applies to the next commit; earlier commits still contain those historical files.

## 4. Update the VPS from GitHub

First configure the template path in Marzban as described in the README. For a **public repository**, SSH into the VPS and download the new template into a temporary file. Replace the GitHub owner, repository, and branch in this URL:

```sh
curl --fail --location --show-error \
  https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/templates/subscription/index.html \
  --output /tmp/circleweb-subscription.html
```

Only continue if curl succeeds. Then back up the installed HTML and replace it:

```sh
sudo mkdir -p /var/lib/marzban/templates/subscription
if [ -f /var/lib/marzban/templates/subscription/index.html ]; then
  sudo cp -a /var/lib/marzban/templates/subscription/index.html "/var/lib/marzban/templates/subscription/index.html.$(date +%Y%m%d-%H%M%S).bak"
fi
sudo install -m 644 /tmp/circleweb-subscription.html /var/lib/marzban/templates/subscription/index.html
sudo marzban restart
```

Check an active subscriber’s HTTPS page and test the import on your device. For a private repository, download from an authenticated clone or use the SCP procedure instead of this public raw URL. To roll back, install a saved `.bak` file over `index.html` and restart Marzban again.

## 5. Optional versioned releases

When a version is ready and committed, create a new tag:

```sh
git tag v1.0.0
git push origin v1.0.0
```

Pushing a tag beginning with `v` triggers the release workflow. After the build and tests pass, it publishes a GitHub Release containing `index.html`, `circleweb-marzban.zip`, and `SHA256SUMS`. Use a new tag for each version. No repository secret is needed; the workflow uses GitHub’s automatic token, with write permission only in its release job.

For a public repository, download a specific released version on the VPS with:

```sh
curl --fail --location --show-error \
  https://github.com/YOUR_USERNAME/YOUR_REPO/releases/download/v1.0.0/index.html \
  --output /tmp/circleweb-subscription.html
```

Then run the backup, install, and restart commands above. Release assets include SHA-256 checksums if you want to verify the downloaded file. Local packages can be regenerated with:

```sh
python3 scripts/build.py
python3 scripts/package.py
```

Outputs are in `dist/` and are excluded from commits.

## Branding and licensing

Third-party font and QR licenses are included alongside their assets. The supplied AradNL font has no license file in this project; confirm its redistribution terms before making the repository public. No open-source license has been assigned to your own code or CircleWeb branding.
