# Ouroboros Pose Editor

A dependency-free, browser-based pose editor for creating and refining an ouroboros composition around Earth.

The editor is built as a single `index.html` file using HTML, CSS, JavaScript, and Canvas 2D.

## Features

- Touch, mouse, trackpad, and keyboard controls
- Individual spline point editing
- Add/delete/duplicate control points
- Whole-snake move and viewport pan modes
- Pinch zoom and pointer-centred wheel zoom
- Depth and perspective controls
- Per-point width controls
- Earth and Moon positioning
- Earth/self-occlusion diagnostics
- Manual topology overrides
- Head, eye, gaze, mouth, neck, and tail controls
- Lighting and illustration shadows
- Reference and closure guides
- Undo/redo
- Autosave
- Named checkpoints
- JSON import/export
- Clean and diagnostic snapshots

## Run locally

No build process or dependencies are required.

Open `index.html` directly in a modern browser.

## GitHub Pages

This repository can be published directly with GitHub Pages:

1. Open **Settings → Pages**
2. Choose **Deploy from a branch**
3. Select `main`
4. Select `/(root)`

The live site will then be available at:

`https://raskal-labs.github.io/ouroboros/`

## Project structure

    ouroboros/
    ├── index.html
    ├── README.md
    ├── LICENSE
    └── .gitignore

## Development

For now, the application intentionally remains a single-file project.

This keeps it easy to:

- run offline
- upload to GitHub Pages
- test on mobile
- copy between editors
- preserve dependency-free operation

If the project becomes substantially larger, the JavaScript and CSS can be split into modules later without changing the browser-based architecture.

## License

See [LICENSE](LICENSE).
