# Detaching a DQF Kaggle run (so you can power off the machine)

**Key fact:** Kaggle notebooks/scripts run on **Kaggle's servers**, not your machine.
Once a run has started, the only thing your laptop does is *watch* it. You can close the
browser and shut down the machine; the run continues server-side.

The thing that *does* kill runs is the **interactive session timeout** (idle sessions are
stopped). So: don't rely on "Run All" in an interactive session for a long unattended run —
use one of the two detached paths below.

---

## Option A — UI: "Save & Run All (Commit)"  ← simplest, no CLI

1. Open the notebook on kaggle.com.
2. Right sidebar, set (they persist in the saved version):
   - **Accelerator:** GPU T4 × 2
   - **Internet:** ON  ← *required*: our scripts fetch input JSON from GitHub raw
3. Top-right **Save Version** → choose **“Save & Run All (Commit)”** → **Save**.
4. You can now close the browser and power off. The notebook runs headless to completion
   (up to the Kaggle session limit) and **outputs are persisted** in the notebook's **Output** tab.

Retrieve later: open the notebook → **Output** tab → download `batchN_verdicts.json`.
(Or `kaggle kernels output rikirinjani/<kernel-slug> -p ./out`.)

## Option B — CLI: `kaggle kernels push` (fully headless)

A `script` kernel runs non-interactively — no browser at all.

```powershell
# 1. make a staging dir with the metadata + the script
mkdir kaggle-push; cd kaggle-push
copy ..\rag-queries\kaggle\kernel-metadata.template.json .\kernel-metadata.json
copy ..\rag-queries\kaggle_batch4_triage.py .
# 2. edit kernel-metadata.json: set a unique "id" (rikirinjani/<new-slug>) and correct "code_file"
kaggle kernels push -p .
# 3. detach immediately; check later from any machine/after reboot:
kaggle kernels status rikirinjani/<new-slug>
kaggle kernels output rikirinjani/<new-slug> -p .\out
```
Credentials live in `~/.kaggle` (already authenticated as `rikirinjani`), so a status/output
check after reboot works without re-login.

> Earlier note in this project said "runs must be started manually in UI". With
> `dataset_sources: []` (we pull input from GitHub raw, not a Kaggle Dataset) `kernels push`
> should start on its own. If it ever doesn't, fall back to Option A.

---

## Made detach-safe in the scripts

`rag-queries/kaggle_batch4_triage.py` (the template for all future triage scripts) now:
- **saves after every group** to `/kaggle/working/batchN_verdicts.json`, and
- **resumes**: on restart it loads the partial output and skips completed groups.

So even if a session is stopped mid-run, re-running the notebook (or the cell) continues from
where it left off instead of starting over.

## Limits (fine for our batches)

- GPU sessions: up to ~12 h; Kaggle weekday GPU quota (~30 h/week). Our triage is ~15–25 min.
- Commit/batch runs are designed to run to completion headless — that's the point.

---

## ⚠️ Caveat: the **L3 evidence fetch is local**

`rag-queries/extract_l3.py` (the RAG/NCBI evidence **fetch**) runs **on this machine** — it
will **not** survive power-off. Only the Kaggle steps (triage/judge) detach.

If you want the fetch to also run while the machine is off, options:
- run `extract_l3.py` on the **Vultr VPS** (it has network + can hold the AWS creds for the
  LanceDB index), or
- run the fetch locally once you're back, then push the triage to Kaggle.

## Checklist before you power off

- [ ] Run started via **Save & Run All (Commit)** (Option A) *or* **`kaggle kernels push`** (Option B)
- [ ] Notebook settings: **GPU T4 ×2** and **Internet ON**
- [ ] First progress line printed (e.g. `input OK: N groups, M sentences`) — confirms it's running server-side
- [ ] Then close browser / shut down — nothing else needed
