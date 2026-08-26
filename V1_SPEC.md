# Ouroboros Pose Editor v1.0.0 — Release Specification

This document is the locked design direction for the first formal release of Ouroboros Pose Editor.

`main` remains the known-good v9.1 pre-release baseline until v1.0.0 is ready. Development occurs on `v1.0.0-dev` and is reviewed through the draft pull request.

## Release identity

- Product version: **1.0.0**
- Git tag: **`v1.0.0`**
- GitHub Release title: **Ouroboros Pose Editor 1.0**
- Release type: stable/latest, not prerelease
- Preserve historical development commits named v5 → v9.1; they do not constrain semantic versioning.

## Hard invariants

- Preserve v9.1 pose behavior unless a v1.0.0 requirement intentionally supersedes it.
- Keep HTML/CSS/JavaScript dependency-free and GitHub Pages compatible.
- No npm, bundler, framework, TypeScript requirement, or build step for the canonical browser version.
- Preserve touch, mouse, trackpad, and keyboard use.
- Preserve point 0 = HEAD, final point = TAIL, semantic direction TAIL → HEAD.
- View pan/zoom remains separate from scene geometry.
- Preserve import compatibility for older supported pose schemas.
- Do not reintroduce the old Length Lock solver or pixel-art post-process.

## Architecture

### Completed foundation

- [x] Preserve `main` at v9.1 while development occurs on `v1.0.0-dev`.
- [x] Split stylesheet from the old monolithic HTML into `css/app.css`.
- [x] Split application JavaScript into `js/app.js`.
- [x] Keep `index.html` as the static GitHub Pages shell.
- [x] Add independent UI-shell and convenience modules/styles for low-risk interface work.

### Target source organization

Continue separating responsibilities as the feature work makes the boundaries useful. Intended domains:

- state/history/import/export/checkpoints
- geometry/spline/projection
- renderer/layers
- topology/occlusion/contact
- interaction/selection/input grammar
- controls/UI shell
- constraints/attachments
- animation

Native browser modules are preferred. The source must remain directly hostable by GitHub Pages.

## Input grammar and selection

Multi-selection is foundational for v1.0.0 rather than an add-on.

- [ ] Plain click selects one control point.
- [ ] Shift-click adds a point to selection.
- [ ] Ctrl/Cmd-click toggles a point in selection.
- [ ] Dragging empty sky can create a marquee selection.
- [ ] Clicking unobstructed sky clears selection and minimizes/collapses the active control panel.
- [ ] Arrow-key nudging acts on the whole selection.
- [ ] Shift keeps the existing larger keyboard nudge step.
- [x] Ctrl/Cmd+Z Undo remains supported.
- [x] Ctrl/Cmd+Shift+Z Redo remains supported.
- [x] Ctrl/Cmd+Y Redo is added for conventional desktop use.
- [ ] Delete/Backspace handles eligible selected body points safely.
- [ ] Input priority must be explicit so wheel zoom/pan/value editing, selection modifiers, dragging, long press, and temporary pan cannot conflict.

### Mouse/trackpad direct value editing

- [ ] Holding/drag-engaging a selected point and using the wheel adjusts the active editable property.
- [ ] The active property is the last focused point property where practical rather than hard-coding Width.
- [ ] Shift+wheel applies the same property adjustment to all selected points.
- [ ] A small transient HUD identifies the active property and value during wheel editing.
- [ ] Wheel elsewhere continues to zoom; Shift+wheel elsewhere continues to pan.

## Batch editing

- [ ] Multi-selection controls display the shared value when equal and a mixed-value state when different.
- [ ] Setting a mixed field assigns the new value to the full selection.
- [ ] Support **Set all to X** and **Add Δ to all** for suitable values, especially Width and Depth.
- [ ] Consider optional selection falloff/soft adjustment after the core selection model is stable.

## Numeric controls

- [x] Existing slider + −/+ + exact numeric entry remains.
- [x] Reset-to-default controls are added for meaningful numeric scene values.
- [ ] Reset behavior must be schema/default aware where a simple initial HTML value is insufficient.

## Control-panel system

- [x] Control-panel backgrounds are translucent by default.
- [x] UI opacity has slider + exact number control.
- [x] UI opacity changes surfaces without reducing text/control legibility.
- [x] Bottom control sheet can be vertically resized by dragging its top edge.
- [x] Control sheet can switch to a floating mode.
- [x] Floating panel can be moved and scaled.
- [x] Floating panel dimensions/position persist locally.
- [x] `…` menu can be moved and resized.
- [ ] Clicking unobstructed sky minimizes/collapses controls without disrupting point interaction.
- [ ] Refine mobile bounds/gesture behavior after real-device testing.

## Head, tail, eyes, and gaze

- [x] Existing head/eye/gaze/mouth/neck/tail controls remain functional.
- [x] Head, gaze, and tail controls are made directly accessible without requiring endpoint selection.
- [ ] Each auxiliary visual gets show/hide where appropriate.
- [ ] Gaze guide/line visibility is independent from gaze-star visibility.
- [ ] Gaze guide supports opacity.
- [ ] Gaze stars support show/hide and opacity.
- [ ] When gaze stars are active, the visible eye gets a restrained sparkle/highlight.
- [ ] Gaze stars are deterministic and concentrated along/around the gaze destination; they do not randomly jump every frame.

## Bite-tail topology state

- [ ] Add explicit **Bite tail** / **Release tail** state; do not infer connection only from visual proximity.
- [ ] Bite-tail constrains the mouth/head relationship to the tail endpoint.
- [ ] While connected, gaze stars disappear automatically.
- [ ] While connected, eye sparkle returns to normal/off.
- [ ] Closure Preview remains useful before committing Bite-tail.
- [ ] Releasing the tail restores the open-serpent state cleanly.

## Preserve Length — replacement for removed Length Lock

Do **not** resurrect the old global solver.

- [ ] Optional mode named **Preserve Length** (or equivalent).
- [ ] Endpoint movement propagates progressively through adjacent control points rather than explosively solving the whole spline.
- [ ] Moving the head propagates head → tail; moving the tail propagates tail → head.
- [ ] Whole-length contraction/extension can operate about the spline midpoint/centre.
- [ ] The user can always disable the constraint and return to Free pose.
- [ ] Constraint behavior must remain stable under ordinary drag, keyboard nudge, and multi-selection edits.

## Depth / perspective system

Depth must read as camera/perspective position, not as a second width control.

- [x] Retain 0..14 depth with 6.5 neutral; larger values are nearer.
- [x] Rename/clarify the UI as **Perspective strength** and explicitly label the FAR ← 6.5 → NEAR meaning.
- [ ] Keep apparent-scale influence as one depth cue.
- [ ] Add a mild positional perspective component around a stable perspective origin/vanishing point.
- [ ] Keep Earth/self-occlusion depth-driven.
- [ ] Add depth-aware cast/contact-shadow cues where meaningful.
- [ ] Near/far shadow offset/softness should help communicate separation from a surface.
- [ ] Width remains anatomical width; Depth/Z remains scene/camera position.

## Earth / Moon attachment and snapping

Use one coherent attachment model rather than separate special-case tools.

- [ ] Points can attach to `none`, `earth`, or `moon`.
- [ ] Support single point, multi-selection, and all-points attachment/snap actions.
- [ ] Snapping projects a point to the relevant visible/spherical surface rather than merely assigning a canned radius.
- [ ] Add Moon contact equivalent to Earth contact.
- [ ] Optional attachment can remain constrained while Earth/Moon moves.
- [ ] Attachment/contact state drives suitable contact shadows.
- [ ] Provide release/detach behavior.

## Layers, visibility, and opacity

Anything primarily visual/non-structural should use a coherent layer model rather than miscellaneous booleans.

Each sensible layer should support:

- [ ] show/hide
- [ ] opacity where partial visibility is useful
- [ ] restoration of its previous opacity after being hidden and shown again

Target layers/groups include, where meaningful:

### Snake

- body
- outline
- head details
- eyes
- eye sparkle
- tail details
- shadows

### Scene

- Earth
- Earth landmasses
- Moon
- ordinary stars
- lighting/shading
- shadows

### Guides

- control points
- point numbers
- direction arrows
- depth labels
- gaze guide
- gaze stars
- reference circle
- mouth↔tail guide
- closure preview

### Topology / diagnostics

- X-ray hidden sections
- behind Earth
- behind snake
- behind both
- crossing markers
- contact markers
- contact shadows
- transition markers

### Presets

- [ ] Editing
- [ ] Clean
- [ ] Diagnostics
- [ ] Minimal
- [ ] Custom

Clean mode should act as a presentation preset/temporary layer override and restore the user’s custom layer state when leaving it.

## Diagnostic colours

Preserve clearly distinct topology states:

- visible snake: normal rendering
- behind Earth: purple
- behind snake: **orange**
- behind both: magenta / crosshatched
- manual forced-front / forced-behind markers remain visually distinct

The connected ribbon renderer must not erase the separate orange snake-behind-snake diagnostic state.

## Renderer cleanup

- [ ] Derive head/tail outline thickness from the same outline system as the body.
- [ ] Make the neck/body ribbon flow under and into the head without a visible outline discontinuity.
- [ ] Make the body/tail-root transition continuous by the same principle.
- [ ] Clip Earth landmasses to the Earth disc/sphere projection so they never escape the globe.

## Checkpoints

- [x] Default checkpoint names are automatically numbered `Checkpoint 001`, `Checkpoint 002`, etc.
- [x] Numbering chooses the next unused integer.
- [x] User can still edit/replace the suggested checkpoint name in the prompt.
- [ ] Consider inline rename in the checkpoint manager after the manager UI is revisited.

## Go mode

Available only while Bite-tail is explicitly connected.

- [ ] Snake travels continuously along its own closed loop rather than deforming the stored pose.
- [ ] Earth rotates independently.
- [ ] Moon orbits independently.
- [ ] Snake speed does not alter Earth rotation or Moon orbital speed.
- [ ] Snake speed uses normalized loop quality rather than raw length alone.
- [ ] Loop quality is based on deviation from a best-fit circle, so an off-centre but circular ouroboros can still achieve maximum speed.
- [ ] Increasing distortion/length reduces snake speed within sane clamps.
- [ ] Releasing the tail exits Go mode safely.
- [ ] Animation includes pause/stop and respects reduced-motion preferences.

## Release criteria

Do not tag/release v1.0.0 until:

- [ ] v9.1 import compatibility is verified.
- [ ] Existing v9.1 editing modes and diagnostics remain usable.
- [ ] Multi-selection/input priority is stable on mouse, trackpad, touch, and keyboard.
- [ ] UI shell works on narrow iPhone-sized layouts and desktop layouts.
- [ ] Depth reads visually as perspective rather than width-only scaling.
- [ ] Preserve Length cannot destabilize/explode the pose.
- [ ] Bite-tail and Go mode are explicitly gated and reversible.
- [ ] Earth/Moon snapping and contact do not silently corrupt topology state.
- [ ] Layer presets preserve and restore user custom settings correctly.
- [ ] Head/body/tail outline continuity is visually consistent.
- [ ] GitHub Pages loads the modular static site without external dependencies or a build step.
- [ ] Final `main` merge is reviewed from the v1.0.0 development PR.
- [ ] Tag `v1.0.0` and publish **Ouroboros Pose Editor 1.0** as the first stable GitHub Release.
