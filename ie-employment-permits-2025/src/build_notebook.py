"""
build_notebook.py
------------------
Executes each analysis cell in-process (pandas/matplotlib), captures
stdout + any matplotlib figures as base64 PNGs, and assembles a valid
.ipynb (nbformat v4) file with real, pre-rendered outputs — so the
notebook renders correctly on GitHub with no need to "Run All".
"""

import io
import json
import base64
import contextlib
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
NB_PATH = ROOT / "notebooks" / "employment_permits_2025_analysis.ipynb"

EXEC_COUNT = 0
GLOBALS = {}
CELLS = []


def _fig_to_output(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=140, bbox_inches="tight")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("ascii")
    return {
        "output_type": "display_data",
        "data": {"image/png": b64, "text/plain": ["<Figure>"]},
        "metadata": {"image/png": {"width": int(fig.get_figwidth() * fig.dpi),
                                    "height": int(fig.get_figheight() * fig.dpi)}},
    }


def md(text):
    CELLS.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(keepends=True),
    })


def code(source):
    global EXEC_COUNT
    EXEC_COUNT += 1
    before = set(plt.get_fignums())

    stdout_buf = io.StringIO()
    outputs = []
    try:
        with contextlib.redirect_stdout(stdout_buf):
            exec(compile(source, "<cell>", "exec"), GLOBALS)
    except Exception as e:
        outputs.append({
            "output_type": "error",
            "ename": type(e).__name__,
            "evalue": str(e),
            "traceback": [f"{type(e).__name__}: {e}"],
        })
        CELLS.append({
            "cell_type": "code",
            "execution_count": EXEC_COUNT,
            "metadata": {},
            "outputs": outputs,
            "source": source.splitlines(keepends=True),
        })
        raise

    text = stdout_buf.getvalue()
    if text:
        outputs.append({
            "output_type": "stream",
            "name": "stdout",
            "text": text.splitlines(keepends=True),
        })

    after = set(plt.get_fignums())
    new_figs = sorted(after - before)
    for num in new_figs:
        fig = plt.figure(num)
        outputs.append(_fig_to_output(fig))
        plt.close(fig)

    CELLS.append({
        "cell_type": "code",
        "execution_count": EXEC_COUNT,
        "metadata": {},
        "outputs": outputs,
        "source": source.splitlines(keepends=True),
    })


def save():
    nb = {
        "cells": CELLS,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    NB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(NB_PATH, "w") as f:
        json.dump(nb, f, indent=1)
    print("Notebook written to", NB_PATH)
