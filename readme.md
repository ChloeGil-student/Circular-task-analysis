<div align="center">

# 🎯 Circular Steering Task — MouseReMoCo analysis

**Reproducing the figures and the performance table of a circular steering task, from raw mouse data**

![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?logo=jupyter&logoColor=white)

*Master IEAP — Python-R-Git course*

</div>

---

## 📌 Overview

This project analyses recordings of the **circular steering task** described in
[Fauviaux et al. (2021)](https://hal.science/hal-03834500), recorded with
[MouseReMoCo](https://github.com/DenisMot/MouseReMoCo).

| # | Goal | Where |
|:-:|---|---|
| 1 | Reproduce the expected figures for the provided recording `001MoDe_R1` | `02_figures` |
| 2 | Re-compute the summary table written by MouseReMoCo at the end of the marker file | `03_analysis` |
| 3 | Run the same code on our own recording (right hand vs left hand) | `04_own_data` |

> **The task** — the participant moves a cursor along a circular track as fast as possible while staying inside it.
> A recording alternates **Record** phases (20 s, analysed) and **Pause** phases (20 s).

---

## 👥 Who did what

| Member | Role | Contributions |
|---|---|---|
| **[Chloé GILLES]** | 🧭 Project manager | Repository setup · reading functions (`src/io_mouse.py`) · `01_load` · `03_analysis` · own recording (participant) · reviews and merges of the pull requests |
| **[Martin PIGEAU]** | 📊 Figures & own data | Plotting functions (`src/plots.py`) · `02_figures` · `04_own_data` · reviews of the pull requests |

### 🌿 Git workflow

Each branch was merged into `main` through a **pull request**, reviewed by the other member and merged by the project manager.
We never worked on the same file at the same time, to avoid merge conflicts.

---

## 🗂️ Repository structure

```
📦 Circular-task-analysis
├── 📁 data
│   ├── 001MoDe_R1.csv           ← provided recording: cursor position over time
│   ├── 001MoDe_R1.marker.csv    ← provided recording: events + MouseReMoCo summary table
│   ├── own_data.csv             ← our recording (6 records: 3 right hand, 3 left hand)
│   └── own_marker.csv           ← markers of our recording
├── 📁 notebooks
│   ├── 01_load.ipynb            ← read the header, samples, markers and record windows
│   ├── 02_figures.ipynb         ← expected figures for 001MoDe_R1
│   ├── 03_analysis.ipynb        ← step-by-step re-computation of the summary table
│   └── 04_own_data.ipynb        ← same analysis on our recording + right vs left hand
├── 📁 src
│   ├── io_mouse.py              ← functions to read MouseReMoCo files
│   └── plots.py                 ← plotting functions
└── 📄 readme.md
```

---

## 🚀 How to run

1. Clone the repository and open its folder in **VS Code**.
2. Open `main.ipynb` and click **Run All**: it runs the 4 notebooks in order (`01` → `04`).
   Each notebook can also be run on its own.

**Requirements**: Python 3 with Jupyter (we used VS Code and the [minimal Python environment](https://github.com/DenisMot/Python-minimal-install) of the course).

| Package | Used for |
|---|---|
| `numpy` | reading the files and computing the statistics |
| `matplotlib` | figures (`pyplot`, `Rectangle`, `Circle`) |
| `ipympl` | interactive figures (`%matplotlib widget`) |
| `os` | paths (Python standard library) |

As asked in the assignment, no other library is used. Our own functions are in `src/` and are imported by the notebooks.

---

## 📈 Results

**✅ `001MoDe_R1`** — the figures match the expected ones, and the re-computed table matches MouseReMoCo's
for the 5 records (largest difference 0.012, the reference being rounded to 2 decimals).

**✅ Own recording** — one right-handed participant, MouseReMoCo 1.3.0, MacBook Air trackpad.
Our values match MouseReMoCo's table for the 6 records (largest difference 0.005).

| Hand | IPe (bit/s) | error (%) | Be | MT/lap (s) |
|---|:-:|:-:|:-:|:-:|
| ✋ Right (dominant) | **9.89** | **2.46** | 0.92 | 4.61 |
| 🤚 Left (non-dominant) | 4.90 | 14.57 | 1.43 | 6.06 |

With the non-dominant hand, `IPe` is about **half** and the error about **6 times higher**,
in the same direction as Fauviaux et al. (2021).

> ⚠️ **Limits** — one participant · hands tested in blocks (right then left) · different screen, target size
> and pointing device than the provided recording.

---

## 📚 References

- Fauviaux et al. (2021) — https://hal.science/hal-03834500
- MouseReMoCo — https://github.com/DenisMot/MouseReMoCo
- Python-for-HMS-Template — https://github.com/DenisMot/Python-for-HMS-Template