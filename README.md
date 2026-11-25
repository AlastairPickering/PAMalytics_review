# PAMalytics — peer-review version

This package contains the source code, demonstration materials and desktop applications for the software described in the accompanying manuscript.

Author identities, institutional details, the public project repository and permanent archive have been withheld during  peer review.

## Reviewer access

The package includes:

- `PAMalytics-review-v1.0.3-macOS-arm64.dmg`
- `PAMalytics-review-v1.0.3-windows-x64-setup.exe`
- anonymised source code in `source/`

No coding or command-line use is required to explore the application.

## macOS

1. Open `PAMalytics-review-v1.0.3-macOS-arm64.dmg`.
2. Drag **PAMalytics Review** into **Applications**.
3. Launch **PAMalytics Review** from Applications.

The macOS application is signed and notarised by Apple.

## Windows

1. Run `PAMalytics-review-v1.0.3-windows-x64-setup.exe`.
2. Launch **PAMalytics Review** from the Windows Start menu.

The Windows installer is unsigned, so Windows may display a security warning. Select **More info**, then **Run anyway**.

## Demonstration project

Both desktop applications contain the same preconfigured acoustic-classification project:

- 48 audio files;
- 589 detections;
- 17 bat species or classes.

The demonstration project is copied into a writable application folder and opened automatically when **PAMalytics Review** starts.

Reviewers can explore the Dashboard and Validation pages immediately. The first opening of the Validation page may take several seconds while PAMalytics prepares the review sample and spectrogram images.

Changes made during validation are stored only in the local reviewer copy of the demonstration project.

## Source code

The `source/` directory contains an anonymised snapshot of the application source and demonstration materials.

Git history, repository metadata and development build outputs are not included.

## Checksums

SHA-256 checksum files are supplied alongside both installers:

- `PAMalytics-review-v1.0.3-macOS-arm64.dmg.sha256`
- `PAMalytics-review-v1.0.3-windows-x64-setup.exe.sha256`
