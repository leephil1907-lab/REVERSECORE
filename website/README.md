# REVERSECORE Website

A responsive, dependency-free static website for the REVERSECORE project.

## Preview locally

From the repository root:

```bash
python -m http.server 8080 --directory website
```

Open `http://localhost:8080`.

## Deployment

The `website/` directory is a static site and can be deployed to any static hosting provider (including Render Static Sites or GitHub Pages). Set the publish/root directory to `website`; no build command is required.

## Notes

- The site introduces the current Python CLI, supported formats, APK inventory, reproducible case files, and optional upstream tools.
- It does not imply that browser-based file uploads or remote analysis are already implemented.
- The quick-start commands are copied from the repository's current README.
- Mobile navigation, active section highlighting, and copy-to-clipboard are implemented in vanilla JavaScript.
