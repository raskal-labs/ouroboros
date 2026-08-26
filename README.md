# Ouroboros Pose Editor

A dependency-free, browser-based pose editor for composing an ouroboros around Earth.

**Current version: v9**  
**Main implementation:** HTML + CSS + vanilla JavaScript + Canvas 2D  
**Build step:** none

## Current status

`main` contains the current v9 editor as a single `index.html` file. The app runs directly in a modern browser and is designed for touch, mouse, trackpad, and keyboard use.

The version history of `index.html` is preserved sequentially as **v5 → v6 → v7 → v8 → v9**.

The substantially different v6 Three.js/WebGL experiment is also preserved on the `threejs-prototype` branch.

## v9 highlights

- Edit / Move / Pan modes
- 0–14 depth system and adjustable perspective
- Earth and Moon positioning/depth controls
- Earth and self-occlusion diagnostics
- Manual crossing/topology overrides
- Per-point width and contact states
- Head, eye, gaze, mouth, neck, and tail controls
- Touch gestures plus mouse/trackpad/keyboard controls
- Undo/redo, autosave, checkpoints, and JSON import/export
- Clean and diagnostic snapshots
- Slider − / + controls with exact numeric entry
- Exact X/Y point controls and keyboard nudging
- Improved multi-crossing topology handling
- Safer long-press/drag state and unlocked-Earth hit testing
- Horizontal Shift+wheel panning and pointer cleanup
- Schema v9 separates head/tail state while retaining older import compatibility

Length Lock and the pixel-art post-process were intentionally removed.

## Run

No dependencies, package manager, build process, or server are required.

Open `index.html` directly in a modern browser.

## GitHub Pages

This repository can be published directly as a GitHub Pages project site from **`main` → `/(root)`**.

When enabled, the site is:

`https://raskal-labs.github.io/ouroboros/`

Because Pages can publish this repository directly, future commits to `main`—for example v10 replacing `index.html`—will automatically become the live version after GitHub Pages redeploys. No copy in `raskal-labs.github.io` is required.

## Repository layout

```text
ouroboros/
├── index.html
├── README.md
├── LICENSE
└── .gitignore
```

## Branches

- `main` — current Canvas 2D editor, currently v9
- `threejs-prototype` — preserved v6 Three.js/WebGL experiment

## License

See [LICENSE](LICENSE).
