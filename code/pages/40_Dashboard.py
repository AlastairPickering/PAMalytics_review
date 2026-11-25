# code/pages/40_Dashboard.py
from pathlib import Path
import sys

import streamlit as st
from code.scripts.dashboard import render_dashboard
from code.utils import build_analysis_dataset as build_ds

THIS_FILE = Path(__file__).resolve()
STUDIO_ROOT = THIS_FILE.parent.parent
if str(STUDIO_ROOT) not in sys.path:
    sys.path.insert(0, str(STUDIO_ROOT))


def _has_streamlit_context() -> bool:
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        return get_script_run_ctx() is not None
    except Exception:
        return False






def _file_signature(path: Path) -> tuple[str, int, int]:
    try:
        stat = path.stat()
        return str(path), int(stat.st_size), int(stat.st_mtime_ns)
    except Exception:
        return str(path), -1, -1


@st.cache_data(show_spinner=False, max_entries=4)
def _load_dashboard_dataset_cached(
    project_path: str,
    norm_sig: tuple[str, int, int],
    enriched_sig: tuple[str, int, int],
    audio_sig: tuple[str, int, int],
):
    return build_ds(Path(project_path), use_stem_fallback=True)


def render_page() -> None:
    st.set_page_config(
        page_title="PAMalytics — Dashboard",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    proj = st.session_state.get("current_project")
    if not proj:
        st.error("No active project. Open a project first.")
        st.stop()

    proj_path = Path(proj)
    data_dir = proj_path / "data_normalised"
    workspace_dir = proj_path / "workspace"
    df_det, _notes = _load_dashboard_dataset_cached(
        str(proj_path),
        _file_signature(data_dir / "detections_normalised.csv"),
        _file_signature(data_dir / "detections_enriched.csv"),
        _file_signature(workspace_dir / "audio_paths.csv"),
    )
    if df_det is None or df_det.empty:
        st.error("No matched detections with audio. Complete Import → Metadata mapping first.")
        st.stop()

    sources = {"project": str(proj_path)}
    st.session_state["pa_df_det"] = df_det
    st.session_state["pa_sources"] = sources
    st.session_state["pa_ready"] = True

    render_dashboard(df_det, sources)


if _has_streamlit_context():
    render_page()
