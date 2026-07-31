"""Build DQF PDF from HTML + figures using weasyprint"""
import os
from weasyprint import HTML

# Paths
BASE = r"C:\Users\think\Project\drug-quantification-framework"
FIGS = os.path.join(BASE, "figures")

html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    @page {{
        size: A4;
        margin: 2cm 2.2cm;
        @top-center {{
            content: "Drug Quantification Framework — Proof of Concept";
            font-size: 8pt;
            color: #888;
        }}
        @bottom-center {{
            content: "Page " counter(page) " of " counter(pages);
            font-size: 8pt;
            color: #888;
        }}
    }}
    body {{
        font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
        font-size: 10pt;
        line-height: 1.5;
        color: #222;
    }}
    h1 {{
        font-size: 22pt;
        color: #1a3a5c;
        border-bottom: 3px solid #4C72B0;
        padding-bottom: 8px;
        margin-top: 30px;
    }}
    h2 {{
        font-size: 15pt;
        color: #2a5a8c;
        border-bottom: 2px solid #ddd;
        padding-bottom: 4px;
        margin-top: 24px;
    }}
    h3 {{
        font-size: 12pt;
        color: #3a6a9c;
        margin-top: 18px;
    }}
    h4 {{
        font-size: 10.5pt;
        color: #444;
        margin-top: 14px;
    }}
    p {{
        margin: 8px 0;
        text-align: justify;
    }}
    .subtitle {{
        font-size: 12pt;
        color: #555;
        margin-top: -10px;
        margin-bottom: 20px;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
        font-size: 9pt;
        page-break-inside: avoid;
    }}
    th {{
        background-color: #4C72B0;
        color: white;
        padding: 7px 8px;
        text-align: left;
        font-weight: bold;
    }}
    td {{
        padding: 5px 8px;
        border-bottom: 1px solid #ddd;
    }}
    tr:nth-child(even) td {{
        background-color: #f8f9fa;
    }}
    tr:hover td {{
        background-color: #e8f0f8;
    }}
    .figure {{
        text-align: center;
        margin: 16px 0;
        page-break-inside: avoid;
    }}
    .figure img {{
        max-width: 100%;
        height: auto;
    }}
    .figure-caption {{
        font-size: 9pt;
        color: #555;
        font-style: italic;
        margin-top: 4px;
    }}
    .note-box {{
        background: #f0f4f8;
        border-left: 4px solid #4C72B0;
        padding: 10px 14px;
        margin: 12px 0;
        font-size: 9pt;
    }}
    .warning-box {{
        background: #fff8f0;
        border-left: 4px solid #DD8452;
        padding: 10px 14px;
        margin: 12px 0;
        font-size: 9pt;
    }}
    .conclusion-box {{
        background: #f0faf0;
        border-left: 4px solid #55A868;
        padding: 12px 16px;
        margin: 16px 0;
        font-size: 10pt;
    }}
    .page-break {{
        page-break-before: always;
    }}
    .small {{
        font-size: 8pt;
        color: #888;
    }}
    ul, ol {{
        margin: 6px 0;
        padding-left: 20px;
    }}
    li {{
        margin: 3px 0;
    }}
    .toc-item {{
        margin: 4px 0;
        padding-left: 10px;
    }}
</style>
</head>
<body>

<!-- Title page -->
<div style="text-align:center; padding-top:120px;">
    <h1 style="border:none; font-size:26pt; margin-bottom:5px;">Drug Quantification Framework</h1>
    <p style="font-size:14pt; color:#666; margin-top:0;">A 4-Level Multi-Dimensional Drug Profiling Framework</p>
    <p style="font-size:11pt; color:#888;">Proof of Concept — NSAID Class</p>
    <div style="margin-top:60px;">
        <p style="font-size:10pt; color:#555;">July 2026</p>
        <p style="font-size:9pt; color:#999;">Built on MedQuery PubMed RAG (27.7M abstracts) + structured PK databases + Cochrane reviews</p>
    </div>
</div>

<div class="page-break"></div>

<!-- Table of Contents -->
<h2>Table of Contents</h2>
<ol>
    <li>Summary</li>
    <li>Framework Architecture</li>
    <li>L1 — Molecular Binding</li>
    <li>L2 — Pharmacokinetics</li>
    <li>L3 — Systems Response</li>
    <li>L4 — Clinical Outcomes</li>
    <li>Clinical Decision Scenarios</li>
    <li>Framework Takeaways</li>
    <li>Limitations</li>
    <li>Methods &amp; Data Sources</li>
</ol>

<div class="page-break"></div>

<!-- Section 1: Summary -->
<h2>1. Summary</h2>

<p>Right now if you compare two analgesics you get a number — NNT, NNH, effect size. That number collapses mechanism, safety, pharmacokinetics, everything into one dimension. But paracetamol and ibuprofen don't share a mechanism, don't share a risk profile, and the "right" choice depends on whether your patient is bleeding, has heart disease, or just needs a tooth pulled. You can't answer that with a single number. The framework keeps all four dimensions separate and lets the question decide the weight.</p>

<p>This proof of concept profiles four analgesics — ibuprofen, diclofenac, celecoxib, and paracetamol — across four levels: molecular binding (L1), pharmacokinetics (L2), systems response (L3), and clinical outcomes (L4).</p>

<table>
<tr><th>Drug</th><th>Role</th><th>Why Selected</th></tr>
<tr><td><b>Ibuprofen</b></td><td>Baseline reference</td><td>Most-studied NSAID, excellent data density across all levels</td></tr>
<tr><td><b>Diclofenac</b></td><td>Complexity</td><td>P2X3 off-target, unique biliary PK — proves multi-axis need</td></tr>
<tr><td><b>Celecoxib</b></td><td>Selectivity</td><td>COX-2 selective — coxib paradox as L3 emergent property</td></tr>
<tr><td><b>Paracetamol</b></td><td>Stress test</td><td>Prodrug (AM404), multi-target, not a true NSAID</td></tr>
</table>

<!-- Figure 1 -->
<div class="figure">
    <img src="file:///{FIGS}/figure1_architecture.png" alt="Framework Architecture" />
    <div class="figure-caption"><b>Figure 1.</b> Drug Quantification Framework — 4-level architecture showing the flow from molecular binding through pharmacokinetics and systems response to clinical outcomes.</div>
</div>

<div class="page-break"></div>

<!-- Section 2: Architecture -->
<h2>2. Framework Architecture</h2>

<p>The framework profiles drugs across four independent levels. Each level is populated from structured databases, literature mining via PubMed RAG, and systematic reviews. Levels are connected by a causal chain (L1→L3→L4) modulated by L2 pharmacokinetics.</p>

<h3>The 4 Levels</h3>

<table>
<tr><th>Level</th><th>What It Captures</th><th>Primary Source</th><th>Key Metrics</th></tr>
<tr>
    <td><b>L1 — Binding</b></td>
    <td>Drug-receptor interaction: primary + off-target</td>
    <td>PDSP + PubMed RAG</td>
    <td>Ki, Kd, IC50, selectivity ratio</td>
</tr>
<tr>
    <td><b>L2 — PK</b></td>
    <td>ADME: absorption, distribution, metabolism, excretion</td>
    <td>Inxight FRDB, DrugBank</td>
    <td>F%, t½, Vd, protein binding</td>
</tr>
<tr>
    <td><b>L3 — Systems</b></td>
    <td>Biological consequences at tissue/pathway level</td>
    <td>Literature (PubMed RAG)</td>
    <td>COX dynamics, tissue duration, off-target engagement</td>
</tr>
<tr>
    <td><b>L4 — Clinical</b></td>
    <td>Human efficacy and safety outcomes</td>
    <td>Cochrane, Oxford League</td>
    <td>NNT, NNH, success rate, stratified by condition</td>
</tr>
</table>

<div class="note-box">
<b>Evidence grading:</b> Every data point tagged with evidence level (HIGH/MODERATE/LOW/VERY LOW) adapted from GRADE, plus confidence qualifiers. See <code>methodology/evidence-hierarchy.md</code>.
</div>

<div class="page-break"></div>

<!-- Section 3: L1 — Binding -->
<h2>3. L1 — Molecular Binding</h2>

<p>Binding affinity profiles reveal that no two drugs in this set share a target profile. Diclofenac has unique P2X3 antagonism (though at micromolar concentrations). Ibuprofen uniquely inhibits ASIC1a allosterically. Paracetamol acts entirely through its metabolite AM404, which is multi-target. Celecoxib is distinguished by COX-2 selectivity (~30:1 vs COX-1).</p>

<div class="figure">
    <img src="file:///{FIGS}/figure2_binding_heatmap.png" alt="Binding Heatmap" />
    <div class="figure-caption"><b>Figure 2.</b> L1 binding profiles. Values are -log₁₀ of IC50/Ki in molar: higher = stronger binding. Zero indicates no measurable activity. The column "COX-2 sel." reflects relative selectivity, not absolute affinity.</div>
</div>

<table>
<tr><th>Target</th><th>Ibuprofen</th><th>Diclofenac</th><th>Celecoxib</th><th>Paracetamol (AM404)</th></tr>
<tr><td>COX-1</td><td>~10 nM</td><td>~5 nM</td><td>~500 nM</td><td>>100 μM</td></tr>
<tr><td>COX-2</td><td>~200 nM</td><td>~5 nM</td><td>~5 nM</td><td>~5 μM (weak)</td></tr>
<tr><td>COX-2 selectivity</td><td>~0.05 (COX-1 pref.)</td><td>~1 (non-selective)</td><td><b>~30:1</b></td><td>Negligible</td></tr>
<tr><td>P2X3</td><td>—</td><td>IC50 76 μM</td><td>—</td><td>—</td></tr>
<tr><td>TRPV1</td><td>~6 μM (inhibition)</td><td>~19 μM (inhibition)</td><td>—</td><td>~1 μM (AM404 agonist)</td></tr>
<tr><td>ASIC1a</td><td>Allosteric inhibition</td><td>—</td><td>—</td><td>—</td></tr>
<tr><td>Nav1.8/1.7</td><td>—</td><td>—</td><td>—</td><td>nM (AM404 block)</td></tr>
<tr><td>CB1</td><td>—</td><td>—</td><td>—</td><td>Indirect (AM404)</td></tr>
<tr><td>PPARγ</td><td>Weak agonist</td><td>—</td><td>—</td><td>—</td></tr>
</table>

<div class="page-break"></div>

<!-- Section 4: L2 — Pharmacokinetics -->
<h2>4. L2 — Pharmacokinetics</h2>

<p>Pharmacokinetic profiles differ substantially across the four drugs. The most clinically relevant distinction is the disconnect between plasma half-life and tissue half-life — diclofenac exemplifies this with 1.2 h plasma t½ but 8-12 h synovial duration. Paracetamol has uniquely low protein binding (20%) and a non-linear toxicity pathway (NAPQI/glutathione depletion). Celecoxib is CYP2C9-dependent, creating a pharmacogenomic vulnerability.</p>

<div class="figure">
    <img src="file:///{FIGS}/figure3_pk_comparison.png" alt="PK Comparison" />
    <div class="figure-caption"><b>Figure 3.</b> Key pharmacokinetic parameters across the four PoC drugs. Vd values shown ×10 for scale visibility; actual values: ibuprofen 0.1 L/kg, diclofenac 1.4 L/kg, celecoxib 5-6 L/kg, paracetamol 0.9 L/kg.</div>
</div>

<table>
<tr><th>Parameter</th><th>Ibuprofen</th><th>Diclofenac</th><th>Celecoxib</th><th>Paracetamol</th></tr>
<tr><td>Bioavailability</td><td><b>100%</b></td><td>65%</td><td>80%</td><td>80%</td></tr>
<tr><td>Vd (L/kg)</td><td>0.1</td><td>1.4</td><td>5-6</td><td>0.9</td></tr>
<tr><td>Protein binding</td><td>99%</td><td>99%</td><td>97%</td><td><b>20%</b></td></tr>
<tr><td>t½ plasma</td><td>1.8 h</td><td>1.2 h</td><td><b>8-12 h</b></td><td>2.0 h</td></tr>
<tr><td>t½ synovial</td><td>4-5 h</td><td><b>8-12 h</b></td><td>~12 h</td><td>N/A</td></tr>
<tr><td>Metabolism</td><td>Glucuronidation + CYP2C9</td><td>CYP2C9 + biliary 30%</td><td><b>CYP2C9 only</b></td><td>Glucuronidation + sulfation</td></tr>
<tr><td>Active metabolite</td><td>No</td><td>Minor</td><td>No</td><td><b>AM404</b></td></tr>
<tr><td>Dosing</td><td>QID-TID</td><td>BID</td><td><b>QD-BID</b></td><td>QID</td></tr>
</table>

<div class="figure">
    <img src="file:///{FIGS}/figure6_pk_disconnect.png" alt="PK Disconnect" />
    <div class="figure-caption"><b>Figure 4.</b> Plasma half-life vs. synovial fluid half-life vs. typical dosing interval. Diclofenac shows the most dramatic disconnect: 1.2 h plasma t½ but 8-12 h synovial t½, explaining why BID dosing works despite rapid plasma clearance. Paracetamol has no COX-mediated duration amplification — its plasma and tissue t½ are equivalent.</div>
</div>

<div class="page-break"></div>

<!-- Section 5: L3 — Systems Response -->
<h2>5. L3 — Systems Response</h2>

<p>The systems level captures the biological consequences of L1 binding expressed at the tissue and pathway level. This is the most novel and least standardized level in the framework — no single structured database captures systems-level pharmacology. Key findings include:</p>
<ul>
<li><b>Diclofenac:</b> Most potent COX inhibition, longest tissue duration, and P2X3 antagonism (partial, at tissue-relevant concentrations)</li>
<li><b>Celecoxib:</b> The coxib paradox — COX-2 selectivity at L1 produces GI-sparing (GOOD) and pro-thrombotic (BAD) at L3, explaining the clinical trade-off at L4</li>
<li><b>Paracetamol:</b> Dual-site mechanism — central (TRPV1→CB1→serotonergic) and peripheral (Nav1.8/1.7 local anesthetic-like block). No anti-inflammatory effect</li>
<li><b>Ibuprofen:</b> ASIC1a off-target inhibition (allosteric) provides COX-independent analgesia — invisible to single-score comparators</li>
</ul>

<div class="figure">
    <img src="file:///{FIGS}/figure5_systems_heatmap.png" alt="Systems Heatmap" />
    <div class="figure-caption"><b>Figure 5.</b> Systems response profiles across 8 dimensions. Scores: 0 = absent, 1 = minimal, 2 = moderate, 3 = strong. Paracetamol scores high on safety dimensions (GI, platelet, endothelial sparing) but zero on COX-dependent dimensions. Diclofenac leads on potency dimensions but scores poorly on safety.</div>
</div>

<div class="page-break"></div>

<!-- Section 6: L4 — Clinical Outcomes -->
<h2>6. L4 — Clinical Outcomes</h2>

<p>NNT (Number Needed to Treat) for ≥50% pain relief over 4-6 hours vs. placebo, with dose-specific values. Safety outcomes are stratified by event type.</p>

<div class="figure">
    <img src="file:///{FIGS}/figure4_nnt_forest.png" alt="NNT Forest Plot" />
    <div class="figure-caption"><b>Figure 6.</b> Forest plot of NNT values with 95% confidence intervals for ≥50% pain relief over 4-6 hours vs. placebo. Dashed reference lines at NNT=2.0 (excellent) and NNT=4.0 (moderate). Paracetamol 1000 mg NNT 3.6 is the weakest performer, but this comparison is misleading when safety dimensions are considered.</div>
</div>

<table>
<tr><th>Drug/Dose</th><th>NNT (95% CI)</th><th>Success Rate</th><th>Source</th></tr>
<tr><td>Ibuprofen 400 mg (fast-acting)</td><td>2.1 (1.9–2.3)</td><td>65%</td><td>Cochrane 2015</td></tr>
<tr><td>Ibuprofen 400 mg</td><td><b>2.5 (2.4–2.6)</b></td><td>54%</td><td>Cochrane 2009 (72 studies)</td></tr>
<tr><td>Ibuprofen 200 mg</td><td>2.7 (2.5–3.0)</td><td>46%</td><td>Cochrane 2015</td></tr>
<tr><td>Diclofenac K 50 mg (fast-acting)</td><td><b>2.1 (1.9–2.5)</b></td><td>~64%</td><td>Cochrane 2015</td></tr>
<tr><td>Diclofenac 50 mg</td><td>2.7 (2.4–3.0)</td><td>~55%</td><td>Cochrane 2009</td></tr>
<tr><td>Celecoxib 400 mg</td><td>2.5 (2.2–2.9)</td><td>~50%</td><td>Cochrane 2008</td></tr>
<tr><td>Celecoxib 200 mg</td><td>3.0 (2.5–3.6)</td><td>~40%</td><td>Moore 2015 overview</td></tr>
<tr><td><b>Paracetamol 1000 mg</b></td><td><b>3.6 (3.2–4.1)</b></td><td>46%</td><td>Cochrane 2008</td></tr>
<tr><td>Paracetamol 500 mg</td><td>3.5 (2.7–4.8)</td><td>32%</td><td>Cochrane 2008</td></tr>
</table>

<h3>Safety Summary</h3>
<table>
<tr><th>Safety Domain</th><th>Ibuprofen</th><th>Diclofenac</th><th>Celecoxib</th><th>Paracetamol</th></tr>
<tr><td>GI bleed risk</td><td>Moderate</td><td><b>Highest</b></td><td>Lowest</td><td><b>None</b></td></tr>
<tr><td>CV risk (chronic)</td><td>Moderate (dose-dep.)</td><td><b>Highest</b></td><td>High</td><td><b>None</b></td></tr>
<tr><td>Hepatotoxicity</td><td>No</td><td>Rare</td><td>No</td><td><b>Yes (NAPQI)</b></td></tr>
<tr><td>Renal risk</td><td>Yes</td><td>Yes</td><td>Yes</td><td>Minimal</td></tr>
<tr><td>Platelet function</td><td>↓ temporary</td><td>↓ temporary</td><td>Normal</td><td>Normal</td></tr>
</table>

<div class="page-break"></div>

<!-- Section 7: Clinical Scenarios -->
<h2>7. Clinical Decision Scenarios</h2>

<p>The following scenarios demonstrate why a multi-axis framework outperforms a single-score comparison. Each "best choice" is derived from the full 4-level profile, not from NNT alone.</p>

<table>
<tr><th>Scenario</th><th>Best Choice</th><th>Why</th><th>Ref</th></tr>
<tr><td>Healthy young adult, acute dental pain</td><td>Ibuprofen 400 mg</td><td>Best NNT (2.5), fast onset, short duration, no chronic safety concern</td><td>[1]</td></tr>
<tr><td>Elderly OA + CV risk</td><td>Paracetamol</td><td>No CV risk — NNT 3.6 but zero thrombotic hazard</td><td>[2]</td></tr>
<tr><td>Elderly OA + GI risk</td><td>Celecoxib + PPI</td><td>COX-2 selectivity spares GI mucosa</td><td>[3]</td></tr>
<tr><td>Severe acute pain, injection needed</td><td>Diclofenac IM</td><td>Most potent COX inhibition, P2X3 adds partial analgesia</td><td>[4]</td></tr>
<tr><td>Patient on warfarin</td><td>Paracetamol</td><td>No platelet effect, no GI bleed risk</td><td>[2]</td></tr>
<tr><td>Renal colic</td><td>Diclofenac IM</td><td>IM formulation + P2X3 in ureteric pain</td><td>[4]</td></tr>
<tr><td>Post-op multimodal</td><td>Paracetamol + ibuprofen</td><td>Different mechanisms → synergy (NNT < 2.0)</td><td>[5]</td></tr>
</table>

<p class="small">[1] Cochrane 2009 PMID:19821340 &nbsp; [2] Mallet 2023 PMID:37016715 &nbsp; [3] SCOT trial PMID:39660078 &nbsp; [4] PMID:39763427 &nbsp; [5] Moore 2015 PMID:26544675</p>

<div class="warning-box">
<b>Key insight:</b> No single score can capture these trade-offs. Paracetamol has the worst NNT but is the safest choice for CV-risk patients. Diclofenac has the best IM efficacy but the highest CV risk. Celecoxib's selectivity is simultaneously its advantage (GI) and disadvantage (CV) — the same molecular feature at L1 produces opposite effects at L4. The framework preserves this complexity rather than collapsing it.
</div>

<div class="page-break"></div>

<!-- Section 8: Takeaways -->
<h2>8. Framework Takeaways</h2>

<h3>What the 4 Levels Reveal (that a single score cannot)</h3>

<ol>
<li><b>Diclofenac vs ibuprofen for acute pain:</b> Same NNT ballpark (2.5 vs 2.7), but diclofenac has P2X3 activity (unique), enterohepatic recirculation (unique), and higher CV risk. A single score can't tell you which to choose for which patient.</li><br/>
<li><b>Celecoxib's paradox:</b> NNT 2.5 — same as ibuprofen. Safer for GI (L4) driven by COX-2 selectivity (L1) → GI COX-1 sparing (L3). Higher CV risk (L4) driven by same feature → PGI2 suppression (L3). The mechanism of both advantage and harm is the same molecular feature.</li><br/>
<li><b>Paracetamol's incommensurability:</b> NNT 3.6 — looks "worse" than ibuprofen's 2.5. But comparing paracetamol to NSAIDs on a single score collapses mechanism, safety, and pharmacokinetics into one dimension — they don't share a mechanism, don't share a risk profile, and the right choice depends on the patient.</li><br/>
<li><b>Ibuprofen's hidden feature:</b> Best NNT among the set (2.5 for 400 mg). Also has ASIC1a activity — invisible to a COX-focused single assay.</li>
</ol>

<h3>Framework Capabilities</h3>
<table>
<tr><th>Capability</th><th>Example</th></tr>
<tr><td>Captures different mechanisms</td><td>Paracetamol's AM404 vs diclofenac's P2X3 vs ibuprofen's ASIC1a</td></tr>
<tr><td>Traces L1→L3→L4 causality</td><td>COX-2 selectivity (L1) → PGI2/platelet imbalance (L3) → CV events (L4)</td></tr>
<tr><td>Handles PK/L3 disconnect</td><td>Diclofenac's 1.2 h plasma t½ → 8-12 h synovial duration</td></tr>
<tr><td>Stratifies by patient</td><td>Same drug, different patient → different profile relevance</td></tr>
<tr><td>Accommodates prodrugs</td><td>Paracetamol→AM404, sulindac, nabumetone</td></tr>
<tr><td>Evidence-graded</td><td>Every data point has PMID, evidence level, confidence</td></tr>
</table>

<div class="page-break"></div>

<!-- Section 9: Limitations -->
<h2>9. Limitations</h2>

<p>The following limitations are structural — they reflect design choices and scope boundaries, not deficiencies to be fixed:</p>

<ol>
<li><b>Domain restriction:</b> PoC covers one drug class (NSAIDs/analgesics) with four drugs. Generalizability to other classes is untested.</li>
<li><b>Selection bias:</b> All four drugs are among the most-studied in pharmacology. Framework viability for drugs with sparse data is unproven.</li>
<li><b>L3 is the weakest level:</b> No structured database exists for systems response. L3 is populated through literature mining, which is labor-intensive and subject to publication bias.</li>
<li><b>Binding affinity variability:</b> Ki values vary by assay conditions (temperature, buffer, species). We report the most commonly cited value, but precision implied by a single number is misleading.</li>
<li><b>Levels are not independent:</b> L1→L3→L4 forms a causal chain. Information is double-counted by design — the causal path is the insight.</li>
<li><b>Emerging evidence:</b> Several findings from 2025-2026 (PNAS 2025 Nav1.8, J Med Chem 2026 COX-1) lack independent replication. Tagged "Emerging."</li>
<li><b>No clinical validation:</b> Claims of improved clinical decision-making are conceptual — no user study or comparison to unaided judgment has been performed.</li>
<li><b>The framework does not rank:</b> It profiles. Rankings require context-specific weights only a user can supply.</li>
</ol>

<div class="page-break"></div>

<!-- Section 10: Methods -->
<h2>10. Methods &amp; Data Sources</h2>

<h3>RAG System</h3>
<table>
<tr><th>Component</th><th>Detail</th></tr>
<tr><td>Endpoint</td><td>balade-pubmed-rag-bot.hf.space</td></tr>
<tr><td>Index</td><td>27.7M PubMed abstracts (1975 – Jan 2026)</td></tr>
<tr><td>Embedding</td><td>bge-small-en-v1.5 (FAISS IVF-PQ)</td></tr>
<tr><td>Reranker</td><td>cross-encoder MiniLM-L-6 (k=3)</td></tr>
</table>

<h3>Structured Data Sources</h3>
<table>
<tr><th>Level</th><th>Primary Source</th><th>Type</th></tr>
<tr><td>L1 Binding</td><td>PDSP Ki database + literature</td><td>Ki values, PMID-tagged</td></tr>
<tr><td>L2 PK</td><td>Inxight FRDB, DrugBank, Lombardo dataset</td><td>ADME parameters</td></tr>
<tr><td>L3 Systems</td><td>PubMed RAG (primary), mechanistic literature</td><td>Pathway/tissue data</td></tr>
<tr><td>L4 Clinical</td><td>Cochrane reviews, Oxford League Table</td><td>NNT/NNH with CIs</td></tr>
</table>

<h3>Evidence Hierarchy</h3>
<table>
<tr><th>Level</th><th>Definition</th><th>Example</th></tr>
<tr><td><b>HIGH</b></td><td>Multiple consistent studies, meta-analyses, established consensus</td><td>Cochrane reviews, large RCTs</td></tr>
<tr><td><b>MODERATE</b></td><td>Replicated findings with some heterogeneity, or single high-quality study</td><td>Binding SAR studies, single RCTs</td></tr>
<tr><td><b>LOW</b></td><td>Single study without replication, in vitro only</td><td>Emerging mechanistic findings</td></tr>
<tr><td><b>VERY LOW</b></td><td>Expert opinion, extrapolated values</td><td>Computational predictions</td></tr>
</table>

<div class="conclusion-box">
<b>Conclusion:</b> The 4-level framework is viable. The most distinctive contribution is the L1 off-target profile + L3 systems response — these are the levels that differentiate drugs within a class where NNT doesn't. The framework does not rank drugs. It fingerprints them. The user asks "for this patient, with this condition, what matters?" — not "which drug is best."
</div>

<hr/>
<p class="small">Drug Quantification Framework — Proof of Concept. July 2026. Full profiles and methodology at drug-quantification-framework/.</p>

</body>
</html>"""

# Write HTML temp file
html_path = os.path.join(BASE, "dqf_poc.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"[OK] HTML written to {html_path}")

# Generate PDF
pdf_path = os.path.join(BASE, "DQF_PoC_NSAID.pdf")
HTML(filename=html_path).write_pdf(pdf_path)
print(f"[OK] PDF generated: {pdf_path}")
print(f"     Size: {os.path.getsize(pdf_path):,} bytes")
