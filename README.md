# PAMalytics — anonymous peer-review version

This repository contains the anonymised source code and demonstration materials for the software described in the accompanying manuscript.

Author identities, institutional details, the public project repository and permanent archive have been withheld during double-anonymous peer review.

## Reviewer demonstration

The included browser-based demonstration uses a preconfigured acoustic-classification project containing:

- 48 audio files;
- 589 detections;
- 17 bat species or classes.

The demonstration supports:

- selection of a validation strategy;
- spectrogram and audio review;
- detection-level validation decisions;
- uncertainty flags;
- validation progress tracking;
- export of reviewed results.

The demonstration data are included only to illustrate the software workflow.

> **Note:** When the validation workflow is opened for the first time, the review sampling strategy may take a few seconds to appear while the app loads and prepares the spectrogram images in the background.

## Run the reviewer viewer

Python 3.12 is recommended.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

On Windows:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Streamlit will open the reviewer viewer in the default web browser.

## Repository contents

```text
streamlit_app.py          Reviewer-facing demonstration entry point
demo_project/             Preconfigured demonstration data and audio
code/                     PAMalytics application source code
docs/                     Supporting documentation
requirements.txt          Python dependencies
pyproject.toml            Project metadata
```

## Testing

Run the source-code smoke test with:

```bash
python -m code.scripts.smoke_test
```

## Licence

The software is provided under the GNU General Public License v3.0. See `LICENSE`.

## Public availability

The public repository, author information and permanent archived release will be provided following completion of double-anonymous peer review.
