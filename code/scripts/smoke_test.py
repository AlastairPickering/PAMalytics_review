import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile


REPO_ROOT = Path(__file__).resolve().parents[2]
DEMO_ROOT = REPO_ROOT / "demo_project"


def fingerprints(root):
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*")) if path.is_file()
    }


def check_page(app, label):
    assert not app.exception, [item.message for item in app.exception]
    assert not app.error, [item.value for item in app.error]
    print(f"{label}: passed", flush=True)


def main():
    assert (3, 12) <= sys.version_info < (3, 13), "Python 3.12 required"
    assert (DEMO_ROOT / "project.json").is_file(), "Bundled demo_project is required"
    assert (REPO_ROOT / "code" / "ReviewHome.py").is_file(), "ReviewHome.py is required"
    before = fingerprints(DEMO_ROOT)
    try:
        with tempfile.TemporaryDirectory(prefix="pamalytics_reviewer_workflow_") as temporary:
            home = Path(temporary)
            project = home / "projects" / "PAMalytics_review_demo"
            shutil.copytree(DEMO_ROOT, project)
            os.environ["PAMALYTICS_HOME"] = str(home)
            os.environ["PAMALYTICS_REVIEW_MODE"] = "1"
            os.environ["PAMALYTICS_REVIEW_PROJECT"] = str(project)
            os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
            os.environ["ARROW_DEFAULT_MEMORY_POOL"] = "system"
            sys.dont_write_bytecode = True
            sys.path[:0] = [str(REPO_ROOT / "code"), str(REPO_ROOT)]

            import numpy as np
            import pandas as pd
            import pyarrow as pa
            from streamlit.testing.v1 import AppTest

            assert np.__version__ == "1.26.4", np.__version__
            assert pa.__version__ == "19.0.1", pa.__version__
            sample = pd.DataFrame({"value": [1, 2], "label": ["a", "b"]})
            pd.testing.assert_frame_equal(pa.Table.from_pandas(sample).to_pandas(), sample)

            original = pd.read_csv(project / "data_normalised" / "detections_normalised.csv")
            assert len(original) == 589, len(original)
            assert original["file_id"].nunique() == 48
            assert original["species_name"].nunique() == 17

            app = AppTest.from_file(str(REPO_ROOT / "code" / "ReviewHome.py")).run(timeout=90)
            check_page(app, "ReviewHome bootstrap")
            assert app.session_state["auth_user"] == "reviewer"
            assert Path(app.session_state["current_project"]).resolve() == project.resolve()
            app.switch_page("pages/40_Dashboard.py").run(timeout=90)
            check_page(app, "Reviewer Dashboard")
            assert len(app.session_state["pa_df_det"]) == len(original)

            app.session_state["validate_num_per_page"] = 2
            app.switch_page("pages/41_Validation.py").run(timeout=90)
            skip = next((item for item in app.button if item.label == "Skip for now"), None)
            if skip:
                skip.click().run(timeout=90)
            check_page(app, "Reviewer Validation")
            current = app.session_state["pa_df_det"]
            assert len(current) == len(original)
            assert {"site", "lat", "lon"}.issubset(current.columns)
            audio_cards = [item for item in app.button if item.label == "Open interactive spectrogram"]
            assert audio_cards, "No demo audio cards were rendered"
            save_controls = [item for item in app.button if item.label == "Mark card as reviewed"]
            assert save_controls, "No review controls were rendered"
            save_controls[0].click().run(timeout=90)
            check_page(app, "Reviewer save")

            saved_path = project / "data_normalised" / "detections_validated.csv"
            saved = pd.read_csv(saved_path)
            assert len(saved) == len(original)
            reviewed = saved["validation_state"].fillna("").ne("")
            assert reviewed.any(), "No submitted reviews were saved"
            assert {"site", "lat", "lon"}.issubset(saved.columns)
            print(json.dumps({
                "detections": len(original), "audio_files": int(original["file_id"].nunique()),
                "species": int(original["species_name"].nunique()), "reviewed_rows": int(reviewed.sum()),
                "numpy": np.__version__, "pyarrow": pa.__version__,
            }), flush=True)
            app.switch_page("pages/40_Dashboard.py").run(timeout=90)
            check_page(app, "Reviewer Dashboard after save")
            assert not any(item.label == "Sign out" for item in app.button)
    finally:
        assert fingerprints(DEMO_ROOT) == before, "Bundled demo files changed"
    print("REVIEWER_WORKFLOW_PASSED; bundled demo unchanged", flush=True)


if __name__ == "__main__":
    main()
