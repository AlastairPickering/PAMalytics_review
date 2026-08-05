# PAMalytics — anonymous peer-review version

This repository contains the anonymised source code and demonstration materials for the software described in the accompanying manuscript.

Author identities, institutional details, the public project repository and permanent archive have been withheld during double-anonymous peer review.

## Reviewer access

Packaged desktop applications are provided separately with the manuscript submission:

- `PAMalytics-v1.0.1-macOS-arm64.dmg`
- `PAMalytics-v1.0.1-windows-x64-setup.exe`

No coding or command-line use is required.

### macOS

Open the DMG, drag PAMalytics into Applications, then launch it from Applications.

The macOS build is signed and notarised by Apple so that it can be installed and launched normally.

> **Double-anonymous review note:** Apple’s code-signing certificate contains the developer’s legal identity in its technical metadata. Reviewers are therefore asked not to inspect the application’s signing certificate or signature details during review.

### Windows

Run the installer, then launch PAMalytics from the Windows Start menu.

The Windows installer is unsigned, so Windows may display a security warning. After confirming that the installer was supplied with the manuscript submission, select **More info** and then **Run anyway**.

## Demonstration project

The `demo_project/` directory contains a preconfigured acoustic-classification project with:

- 48 audio files;
- 589 detections;
- 17 bat species or classes.

To explore the demonstration:

1. Install and open PAMalytics.
2. Open the included `demo_project` folder.
3. Launch the dashboard.
4. Explore the Dashboard, Validation and Recalculate pages.

When the validation workflow is opened for the first time, the review sampling strategy may take a few seconds to appear while PAMalytics loads and prepares the spectrogram images.

## Source code

The anonymised application source code is included in the `code/` directory for reviewer inspection.

## Repository contents

```text
code/                     PAMalytics application source code
demo_project/             Preconfigured demonstration project and audio
docs/                     Supporting documentation
requirements.txt          Python dependencies
pyproject.toml            Project metadata