# RAGBench Multi-Domain Evaluation — Presentation Script

**Total speaking time target: ~13:30 (buffer shrinks to ~1:30 for Q&A/setup — see Timing Summary at the bottom)**
**Team:** Pritvish (Biomedical) · Venkat (Legal) · Dhananjay (Financial) · Arhan (General Knowledge)
**Design brief for Claude Design:** Light theme, Geist Mono (or closest monospace/geometric-sans fallback) for headers and data labels, colorful-but-professional palette — assign one accent color per domain and reuse it consistently across both of that domain's slides, charts, and table headers. Suggested accents: Biomedical = teal/green, Legal = navy/gold, Financial = burgundy/amber, General Knowledge = purple/cyan. The 5 shared/framework slides (Title, Agenda, Problem & Objective, Dataset & Framework, Pipeline Architecture, Key Takeaways, Limitations & Next Steps, Questions) should use a neutral fifth accent (e.g. charcoal/slate) so they read as "the frame" around the four domain stories, not a fifth domain. Keep body font a clean sans-serif for readability; reserve Geist Mono for config names, metric numbers, and code-like tokens (e.g. `v8c`, `rrf_k=30`) so the "config as data" feel comes through.

**Recurring chart pattern (use on every domain's 2nd slide, for visual consistency across the deck):** a combo chart per domain — grouped bars for the 3 continuous metrics (Relevance RMSE, Utilization RMSE, Completeness RMSE — lower is better, left axis 0–0.7) across the 3 featured iterations, plus a line overlay for Adherence AUCROC (higher is better, right axis 0–1, dashed line at 0.5 = "random guessing" as a visual anchor). This single chart type repeated 4× (once per domain) is what makes the "compare and contrast across domains" ask land — by the final slide the audience already knows how to read it.

**Animation/build guidance (apply throughout, not just where called out):** default to progressive reveal — bullets, table rows, and chart series should build in one at a time as the speaker reaches that point, not appear all at once. Chart bars/lines animate in left-to-right in the order the speaker narrates them. Diagrams (pipeline, problem-framing) build stage-by-stage. This keeps the audience's eyes synced to the narration instead of reading ahead.

---

## SLIDE 0 — Title

**On-slide text:**
> Evaluating RAG Pipelines Across Domains
> A Multi-Domain RAGBench Study: Biomedical · Legal · Financial · General Knowledge
> [Team names] — Capstone Project 2026

**Visual aid:** Full-bleed light background, four small domain icons (stethoscope/DNA helix, gavel/scale, ledger/currency, globe/lightbulb) arranged around the title, each pre-tinted in that domain's accent color — a visual promise of what's coming.

**Speaker (whoever opens):** *(~15s, ~35 words)*
"Good [morning/afternoon]. Today we're presenting a capstone project where four of us each built and iteratively tuned a RAG pipeline against RAGBench, across four very different domains, using the same rigorous evaluation framework: TRACe."

---

## SLIDE 1 — Agenda & Team

**On-slide text:**
- **What we'll cover:** the problem we're solving → our shared dataset & framework → our shared pipeline architecture → four domain deep-dives (config evolution, top runs, results) → cross-cutting takeaways → limitations & next steps
- **Four domains, four presenters:**

  | Presenter | Domain | Dataset(s) |
  |---|---|---|
  | Pritvish | Biomedical | RAGBench covidqa + pubmedqa |
  | Venkat | Legal | RAGBench CUAD |
  | Dhananjay | Financial | RAGBench FinQA + TatQA |
  | Arhan | General Knowledge | RAGBench hotpotqa + msmarco |

**Visual aid:** Simple horizontal roadmap/breadcrumb graphic across the top of the slide — 7 small numbered nodes (Problem → Data/Framework → Architecture → 4 Domains → Takeaways → Limitations → Q&A) — this same roadmap graphic can reappear, greyed-out with the current node highlighted, as a small strip at the top of every subsequent section-opening slide, so the audience always knows where they are.

**Speaker:** *(~30s, ~75 words)*
"Here's the shape of the next several minutes. We'll start with the problem we're actually solving and why RAG evaluation is hard in the first place, then walk through the shared dataset and framework, and the shared pipeline architecture all four of us built on top of. Then each of us takes two slides for our domain — the configuration journey, the top runs, the results. We'll close with cross-cutting takeaways, limitations, and next steps."

---

## SLIDE 2 — Problem & Objective

**On-slide text:**

**Title:** Why Evaluating RAG Is Hard — And What We Set Out to Prove

**The problem:**
- A RAG system's output is *fluent by default* — a hallucinated answer and a well-grounded one can read identically to a human skimming it
- Traditional NLP metrics (BLEU, ROUGE, exact-match accuracy) score surface similarity to a reference answer — none of them can tell "confidently wrong" apart from "correctly grounded in the retrieved evidence"
- This isn't a cosmetic gap: in biomedical, legal, and financial domains specifically, an ungrounded-but-fluent answer is a real-world risk, not just a quality nitpick

**Our objective:**
- Build four independent RAG pipelines across four real-world domains, evaluate all of them with the same rigorous, sentence-level framework (TRACe), and discover — empirically, not by intuition — which configuration levers actually move the needle
- Methodology constraint every team held to: **one variable changed per iteration**, a hypothesis stated *before* the run, and explicit confirm/falsify criteria checked *after* — no batch sweeps, no cherry-picking a good-looking result

**Visual aid:** Two-panel "what looks right vs. what's actually verified" infographic. Left panel: a fluent 3-sentence generated answer, plain black text, a green checkmark badge in the corner labeled "Looks correct." Right panel: the *same* 3 sentences, but sentence-by-sentence color-coded — green underline for sentences traceable to a retrieved document, red underline for a sentence that isn't — labeled "Is it actually grounded?" **Animation:** the red/green underlines fade in one sentence at a time as the speaker says the corresponding line, ending on the red sentence being circled/highlighted as the punchline ("this is the one a surface metric would never catch").

**Speaker notes:** *(~45s, ~110 words)*
"Here's the core problem with evaluating any RAG system: the output is fluent by default. A hallucinated sentence and a well-grounded one can look identical to someone just reading the answer — and standard NLP metrics like BLEU or exact-match accuracy only measure similarity to a reference answer, not whether each claim is actually traceable to the retrieved evidence. In biomedical, legal, and financial contexts specifically, that gap is a real risk, not a nitpick. So our capstone's objective was simple to state and hard to execute: build four independent pipelines across four domains, evaluate all of them with the same sentence-level framework, and find out empirically — one variable at a time — which configuration choices actually matter."

---

## SLIDE 3 — Dataset & Framework

**On-slide text:**

**Title:** One Benchmark, One Framework, Four Domains

**Dataset — RAGBench (`galileo-ai/ragbench`):**
- A unified benchmark spanning multiple real-world corpora, each pre-annotated by expert humans with ground-truth relevance / utilization / completeness / adherence labels — so every pipeline's predictions can be checked against a real answer key, not just against each other

| Domain | RAGBench source(s) | Document character |
|---|---|---|
| Biomedical | covidqa, pubmedqa | Dense clinical/research literature |
| Legal | CUAD | Contract clauses, hedged legal language |
| Financial | FinQA, TatQA | Financial reports — tables + narrative text |
| General Knowledge | hotpotqa, msmarco | Multi-hop reasoning + single-hop factoids |

**Framework — TRACe (Relevance, Utilization, Completeness, Adherence):**
- **Relevance** — fraction of retrieved sentences actually relevant to the question *(RMSE ↓)*
- **Utilization** — fraction of retrieved sentences the response actually used *(RMSE ↓)*
- **Completeness** — of the relevant sentences, how many made it into the response *(RMSE ↓)*
- **Adherence** — is every response sentence fully supported by the context — the hallucination check *(AUCROC ↑, 0.5 = random guessing)*

**Visual aid:** A 4-icon horizontal strip — magnifying glass (Relevance), puzzle-piece-fitting-in (Utilization), checklist-with-ticks (Completeness), shield-with-checkmark (Adherence) — each icon sitting above its one-line definition and its scoring method as a small pill/badge ("RMSE ↓" ×3, "AUCROC ↑" on the last one, visually distinct color to flag it's the odd one out). **Animation:** icons animate in left to right as the speaker names each metric in turn.

**Speaker notes:** *(~45s, ~105 words)*
"All four of us evaluated against RAGBench — a single benchmark that spans multiple real-world corpora, each already annotated by expert humans with a genuine ground-truth answer key. That's what let every team score their pipeline's predictions against real values, not just eyeball them. And all four of us scored those predictions the same way, using RAGBench's own TRACe framework: relevance and utilization measure retrieval quality, completeness measures coverage, and adherence — scored via AUCROC rather than RMSE, since it's fundamentally a yes-or-no hallucination check — is the metric we'll come back to again and again, because it's the one that actually catches confident-but-wrong answers."

---

## SLIDE 4 — Pipeline Architecture

**On-slide text:**

**Title:** One Shared Architecture, Tuned Four Ways

**End-to-end flow (shared by all four domains):**
1. **User Question** →
2. **Hybrid Retriever** — dense embedding search + BM25 keyword search, fused via Reciprocal Rank Fusion (RRF) →
3. **MMR Diversity Selection** — trims redundant/overlapping candidates →
4. **Cross-Encoder Reranker** — precisely reorders the surviving candidates →
5. **Top-k Documents** passed to both the generator and the judge →
6. **Generator LLM** — produces the actual response →
7. **Independent Judge LLM** — sentence-by-sentence annotation: is each context sentence relevant? was it utilized? is each response sentence fully supported? →
8. **TRACe Metrics Engine** — computes RMSE (relevance/utilization/completeness) and AUCROC (adherence) against RAGBench's own ground truth →
9. **Scoreboard**

**Fixed across all four domains:** TRACe scoring formulas, generator/judge independence, RMSE/AUCROC comparison methodology
**Tuned per domain:** embedding model, chunking strategy, `top_k`, MMR λ, reranker on/off, generation prompt style — this is exactly what the next 8 slides walk through

**Visual aid:** Horizontal flow diagram, 6–7 boxes connected by arrows, color-coded by stage type — retrieval stages in blue, generation in green, judge in amber, scoring in purple. A dashed bracket under boxes 2–4 labeled "tuned per domain" and another under the judge/scoring boxes labeled "held fixed for every team." **Animation:** boxes build in left-to-right, one per narrated stage, with the "tuned per domain" and "held fixed" brackets fading in last as a summary beat.

**Speaker notes:** *(~50s, ~120 words)*
"Every one of our four pipelines shares this same shape. A question comes in, hybrid retrieval combines dense embedding search with BM25 keyword search, MMR trims redundant candidates, and a cross-encoder reranker does the final precision pass — that's the retrieval side. The surviving top-k documents go to two places: a generator LLM that writes the actual answer, and a completely independent judge LLM that annotates, sentence by sentence, what was relevant, what was used, and what's actually supported. Everything downstream of that — the TRACe formulas, the RMSE and AUCROC scoring, generator/judge independence — was held fixed across all four of us. What each team tuned is the retrieval-side knobs: embedding model, chunking, top-k, MMR settings. That's exactly what you're about to see, one domain at a time."

---

## SLIDE 5 — Biomedical (Pritvish), Slide 1 of 2: Objective & Methodology

**On-slide text:**

**Title:** Biomedical — Grounding Answers in Clinical & Research Literature

**Why it matters:**
- Domains: covidqa + pubmedqa — dense, technical biomedical text where a hallucinated claim is a patient-safety-adjacent risk, not just an inconvenience
- Adherence (hallucination detection) is the make-or-break metric here — more than in any other domain, "sounds plausible" and "is supported by the source" diverge

**Methodology at a glance:**
- 40 iterations, single-lever-at-a-time, all levers on the retrieval side (embedding, reranker, chunking, top-k, RRF, MMR) — generator and judge prompts held fixed throughout
- Major mid-project correction: discovered generation was unseeded, meaning several early "best results" were lucky draws, not real config effects — added `seed=42` and re-validated everything that mattered
- All three of this project's own "best" configs share one recipe — whole-document retrieval (no chunking), `use_mmr=True` (λ=0.5), `top_k_final=5`, reranker on, `"long"` prompt, `seed=42` — and differ *only* in scope and `top_k_retrieve`

**Top 3 best runs (each the winner for a different scope):**

| Config | Scope | `top_k_retrieve` | Relevance RMSE ↓ | Utilization RMSE ↓ | Completeness RMSE ↓ | Adherence AUCROC ↑ |
|---|---|---|---|---|---|---|
| `v8c` | Best pubmedqa-only | 20 | 0.276 | 0.121 | **0.242** | 0.923 |
| `v8l` | Best covidqa-only (seeded) | 30 | **0.269** | **0.103** | 0.443 | **0.929** |
| `v8e` (final, presented) | Best cross-domain (both together) | 20 | 0.321 | 0.149 | 0.399 | 0.870 |

**Speaker notes:** *(~65s, ~160 words)*
"In biomedical QA, a fluent but ungrounded answer is the worst possible failure mode — so adherence, our hallucination-detection metric, was our north star. We ran 40 config iterations, changing exactly one retrieval-side lever at a time, while keeping the generator and judge prompts completely fixed as a hard constraint. Partway through, we caught a real methodology bug: our generation calls weren't seeded, so a couple of our early 'best results' turned out to be lucky random draws, not real effects — we fixed that with `seed=42` and re-validated everything that mattered. What we ended up with are three 'best' configs, one per scope, all sharing the same core recipe — whole-document retrieval plus MMR — but differing in how many candidates we retrieve before reranking. `v8c` is our best pubmedqa-only result; `v8l` widens the candidate pool to 30 for covidqa's longer documents and gets our single best adherence score, 0.929. But neither generalizes safely to both domains at once — that's what `v8e` is for, and it's the config we're presenting as final."

---

## SLIDE 6 — Biomedical (Pritvish), Slide 2 of 2: Key Findings & Conclusion

**On-slide text:**

**Title:** Biomedical — What 40 Iterations Taught Us

**[CHART — combo bar+line, per the recurring pattern]**
X-axis: `v8c` (pubmedqa-best) → `v8l` (covidqa-best) → `v8e` (cross-domain final)
Bars (left axis, 0–0.5): Relevance RMSE, Utilization RMSE, Completeness RMSE
Line (right axis, 0–1, dashed reference at 0.5): Adherence AUCROC
*Visual story the chart should tell: `v8c` and `v8l` each post the best number for their own domain (note completeness swings up for `v8l` — a real domain tradeoff, not noise); `v8e`'s bars/line sit in between both, showing the cost of a single config covering both domains at once.*

**Key findings:**
- **MMR was the single most impactful lever tested across the whole 40-iteration sweep** — bigger than embedding model, reranker choice, chunking, or top-k changes combined (+0.25 AUCROC vs. the pre-MMR baseline)
- **Chunking consistently hurt adherence**, regardless of chunk size (500–1200 chars) — whole-document retrieval preserves the context a generator needs to stay grounded
- **`top_k_retrieve` is domain-specific, not universal**: widening it to 30 is what makes `v8l` covidqa's best config, but the same value collapses pubmedqa's adherence (0.92 → 0.56) — no single value wins both, so the cross-domain config (`v8e`) uses the safer value (20)
- **Domain-adapted embeddings/rerankers (PubMedBERT, MedCPT) underperformed** general-purpose models — a genuinely counterintuitive result worth flagging

**Conclusion:** Final cross-domain config (`v8e`) = whole-document retrieval + MMR (λ=0.5) + reranker + `top_k=20/5`, seeded. **Relevance 0.321 · Utilization 0.149 · Completeness 0.399 · Adherence 0.870** — near the top of RAGBench's own reported range for comparable judges. `v8c`/`v8l` remain the reference points for anyone deploying single-domain, not cross-domain.

**Speaker notes:** *(~65s, ~160 words)*
"This chart puts our three best configs side by side. `v8c` and `v8l` are each the single best result for their own domain — but notice they're not the same config: `v8l` widens the retrieval candidate pool to 30 documents, which is exactly what covidqa's longer documents need, and pushes adherence to our project-best 0.929. Try that same setting on pubmedqa, though, and adherence collapses from 0.92 down to 0.56 — so there is no universal top-k value. That's precisely why `v8e` exists: it's the safer, shared setting that performs well on both domains at once rather than being the single best on either. Two other findings worth flagging: chunking hurt adherence at every chunk size we tried, and swapping in biomedical-specific embedding and reranker models — which we expected to help — actually made things worse. The lever that mattered most, by far, was simply turning MMR on. Our final recommended cross-domain config lands at 0.87 adherence AUCROC — near the top of RAGBench's own published range."

---

## SLIDE 7 — Legal (Venkat), Slide 1 of 2: Objective & Methodology

**On-slide text:**

**Title:** Legal — Extracting Precise Clauses Without Overreach

**Why it matters:**
- Domain: CUAD (Contract Understanding Atticus Dataset) — legal clause extraction, where completeness (did we surface every relevant clause?) and adherence (did we invent contract language?) are both high-stakes
- The core tension in this domain: verbose, hedged legal language improves completeness but tends to tank adherence — the "RAG Tradeoff Triangle"

**Methodology at a glance:**
- 35 iterations sweeping prompt style (Concise → Long CoT → JSON CoT → custom "Dual-Track"), retrieval architecture (Hybrid, Parent-Child), chunk size, and generator/judge model choice
- Fixed throughout: judge model (Llama-3.1-8B, until a controlled 120B judge test), judge prompt template, dataset split, n=20, seed
- Key structural insight that shaped the whole sweep: a custom JSON-based "Dual-Track" prompt — forcing hidden reasoning before a single extracted answer — was hypothesized to escape the tradeoff triangle other prompt styles couldn't

**Top 3 iterations — the trajectory:**

| Config | Key change | Relevance RMSE ↓ | Utilization RMSE ↓ | Completeness RMSE ↓ | Adherence AUCROC ↑ |
|---|---|---|---|---|---|
| `v0_baseline` | Dense retrieval, Long CoT prompt | 0.442 | 0.315 | 0.602 | 0.395 |
| `v18_ensemble_mmr_rich` | +Hybrid+MMR retrieval, Dual-Track prompt | 0.296 | **0.055** | 0.577 | 0.845 |
| `v19_colleague_hybrid_rich` (final) | +chunk_size=800 "Goldilocks" tuning | 0.297 | 0.060 | 0.552 | 0.810 |

**Speaker notes:** *(~65s, ~160 words)*
"Legal clause extraction has a very specific failure mode: contract language is dense and hedged, so a generator that writes naturally-verbose responses looks *complete* but often *invents* qualifying language that isn't actually in the contract. We call this the RAG Tradeoff Triangle — utilization efficiency versus adherence safety. We ran 35 iterations across prompt style, retrieval architecture, and chunk size, holding the judge model and prompt fixed. Our baseline used a standard Long Chain-of-Thought prompt and dense retrieval — adherence was below a coin flip at 0.395, meaning our hallucination detector was actively unreliable. The breakthrough came from combining Hybrid-plus-MMR retrieval with a custom prompt we call 'Dual-Track' — it forces the model to reason inside a hidden JSON structure but only output one clean extracted clause, which pushed adherence to 0.845 while cutting utilization error by nearly six-fold. Our final config then tuned chunk size to 800 characters, landing on what we call the production equilibrium."

---

## SLIDE 8 — Legal (Venkat), Slide 2 of 2: Key Findings & Conclusion

**On-slide text:**

**Title:** Legal — Escaping the RAG Tradeoff Triangle

**[CHART — combo bar+line, per the recurring pattern]**
X-axis: `v0_baseline` → `v18_ensemble_mmr_rich` → `v19_colleague_hybrid_rich` (final)
Bars (left axis, 0–0.7): Relevance RMSE, Utilization RMSE, Completeness RMSE
Line (right axis, 0–1, dashed reference at 0.5): Adherence AUCROC
*Visual story: utilization RMSE collapses from 0.32 to ~0.06 between baseline and `v18`; adherence line rockets from below the 0.5 dashed line to above 0.8 and holds there.*

**Key findings:**
- **Standard prompt engineering alone cannot escape the tradeoff triangle** — every "Paper Baseline" style variant (short, JSON CoT, few-shot) traded completeness for adherence or vice versa
- **Structural JSON decoupling (Dual-Track) was the only lever that broke the tradeoff** — separating "reasoning space" from "output space" let the model stay grounded *and* concise simultaneously
- **A 120B judge model was tested and rejected**: over-strict semantic judgment penalized *correct* answers, proving judge calibration matters as much as judge capability
- **Chunk size 800 chars is the sweet spot**: matches human-annotator response density (utilization RMSE ≈ 0.06) without the adherence cost of larger or smaller chunks

**Conclusion:** Final config = Hybrid+RRF retrieval, chunk_size=800, custom Dual-Track prompt. **Relevance 0.297 · Utilization 0.060 · Completeness 0.552 · Adherence 0.810** — the best all-around production balance found across 35 configs.

**Speaker notes:** *(~65s, ~160 words)*
"This chart makes the tradeoff-triangle story visible: every earlier config either had good utilization or good adherence, never both — until `v18`. That's where utilization RMSE falls off a cliff and the adherence line crosses above our 0.5 random-guessing baseline for good. The key insight is *why*: it wasn't retrieval tuning or judge swapping that broke the tradeoff — it was restructuring the *prompt itself* to separate the model's hidden reasoning from its final output. We also want to flag a negative result: we tested a much larger 120-billion-parameter judge model, expecting better calibration, and got the opposite — it was hyper-strict and penalized genuinely correct answers, hurting adherence. Bigger isn't automatically better calibrated. Our final config settles on an 800-character chunk size, which happens to match human annotators' response density almost exactly. This is our recommended production configuration: strong relevance, excellent utilization, and adherence above 0.81."

---

## SLIDE 9 — Financial (Dhananjay), Slide 1 of 2: Objective & Methodology

**On-slide text:**

**Title:** Financial — Numerical Precision Under an Independent Judge

**Why it matters:**
- Domains: FinQA (financial-report QA over tables and text) + TatQA (tabular + textual QA) — questions demand multi-step arithmetic ("rate of return," "% change") where a single wrong number is a hard failure, not a nuance
- Judge independence is the central story here: an early config used the *same* model as both generator and grader — like grading your own exam

**Methodology at a glance:**
- FinQA track: 3 clean iterations (`v2`→`v3`→`v4`), each isolating exactly one variable, plus later diagnostic robustness checks (RGB noise-robustness, negative rejection)
- TatQA track: reused FinQA's proven levers, then independently tuned retrieval depth and sampling strategy for TatQA's much shorter documents
- Fixed throughout: dataset splits, generator model, decoding params; only judge model and embedding model changed across the featured iterations

**Top 3 iterations — the trajectory (FinQA):**

| Config | Key change | Relevance RMSE ↓ | Utilization RMSE ↓ | Completeness RMSE ↓ | Adherence AUCROC ↑ |
|---|---|---|---|---|---|
| `v2` (baseline) | Generator = Judge (self-evaluation) | 0.296 | 0.347 | 0.444 | 0.429 |
| `v3` | **Independent judge model** | 0.098 | 0.078 | 0.248 | 0.714 |
| `v4` (final) | +larger embedding model | 0.122 | 0.112 | **0.186** | **0.786** |

**Speaker notes:** *(~65s, ~160 words)*
"Financial QA is unforgiving of arithmetic mistakes — 'what was the rate of return' has exactly one right answer, no room for a plausible-sounding approximation. Our starting baseline, `v2`, made a subtle but critical mistake: it used the same model to both generate and grade its own answers — like a student marking their own exam. The result was an adherence score of 0.429, *worse than random guessing* — the self-grading bias was actively inverting our hallucination signal. Swapping to a genuinely independent judge model in `v3` was the single largest jump in the entire financial track: every metric improved dramatically, with adherence nearly doubling to 0.714. `v4` then isolated the embedding model as the next lever, upgrading to a larger embedding — completeness improved further and adherence reached 0.786, though relevance and utilization saw a small, real tradeoff. We ran the same disciplined process on TatQA, reusing these proven levers and separately tuning for its shorter documents."

---

## SLIDE 10 — Financial (Dhananjay), Slide 2 of 2: Key Findings & Conclusion

**On-slide text:**

**Title:** Financial — Judge Independence Is the Dominant Lever

**[CHART — combo bar+line, per the recurring pattern]**
X-axis: `v2` (baseline) → `v3` (independent judge) → `v4` (final)
Bars (left axis, 0–0.5): Relevance RMSE, Utilization RMSE, Completeness RMSE
Line (right axis, 0–1, dashed reference at 0.5): Adherence AUCROC
*Visual story: all three bars fall sharply at `v3`; the adherence line starts below the 0.5 dashed line at baseline and climbs steadily through `v3` into `v4`.*

**Secondary domain validation — TatQA final config (`tatv3`):**
Relevance 0.157 · Utilization 0.160 · Completeness 0.397 · Adherence 0.558 — confirms the same judge-independence + embedding-upgrade levers transfer to a second financial dataset, with `top_k` re-tuned for TatQA's shorter documents.

**Key findings:**
- **Self-evaluation bias is real and severe** — same-model grading suppressed hallucination detection *below chance*; independent judging alone nearly doubled it
- **Embedding quality is a genuine tradeoff, not a free upgrade** — `v4`'s larger embedding improved completeness/adherence but slightly cost relevance/utilization versus `v3`
- **A recurring judge quirk found across both domains**: the judge is inconsistently lenient on harmless "scaffolding" sentences (e.g., "to find X, we need Y") — a rule-based fix was tried and explicitly *rejected* after it also forgave a real hallucination
- **Retrieval-ranking sophistication (hybrid search, MMR, reranking) mattered far less than judge/embedding choice** in this domain

**Conclusion:** Final config = independent judge (`gpt-oss-120b`) + larger embedding + hybrid/MMR/rerank retrieval. **FinQA: Adherence 0.786** (top of RAGBench's reported range) · **TatQA: Adherence 0.558**, both judge-independence-validated.

**Speaker notes:** *(~65s, ~160 words)*
"The chart tells one clear story: nearly the entire improvement in this domain happens in one step, at `v3`. That's the judge-independence effect — and it's the headline finding of our whole financial track. We also want to be transparent about a limitation we found and *rejected fixing*: our judge is inconsistently lenient on harmless transition sentences, like 'to find X we need Y.' We tried a rule-based patch to forgive these automatically, tested it, and it made things worse — it also forgave one of our genuinely hallucinated responses, so we kept the stricter, imperfect judge rather than a falsely lenient one. That's a real methodological discipline point: not every identified issue gets a fix if the fix causes more harm. Our final configuration pairs an independent judge with a larger embedding model, reaching 0.786 adherence on FinQA — at the top of RAGBench's own reported range — and we confirmed the same levers transfer to TatQA."

---

## SLIDE 11 — General Knowledge (Arhan), Slide 1 of 2: Objective & Methodology

**On-slide text:**

**Title:** General Knowledge — Multi-Hop Reasoning vs. Single-Hop Factoids

**Why it matters:**
- Domains: hotpotqa (multi-hop reasoning, needs 2+ documents chained together) + msmarco (single-hop factoid lookup) — a genuine domain-asymmetry stress test within one presentation
- The central problem: baseline adherence for hotpotqa was *below chance* (0.393) — our hallucination detector was structurally failing on multi-hop questions specifically

**Methodology at a glance:**
- 41 iterations — the widest sweep of any domain — spanning chunking strategy, top-k, MMR lambda, temperature, and prompt style, isolating a **dominant confound**: random seed/sample selection, more influential than any single config lever
- Fixed throughout: judge model, judge prompt, dataset split; every iteration logged both per-domain and pooled results to track the hotpotqa/msmarco asymmetry directly

**Top 3 iterations — the trajectory:**

| Config | Key change | Hotpotqa Adherence ↑ | Msmarco Adherence ↑ | Notes |
|---|---|---|---|---|
| `v0_baseline` | Long CoT, dense+hybrid+MMR | 0.393 (below chance) | 0.821 | The problem, quantified |
| `v4_hotpotqa` | Sentence-window chunking (400/4) + MMR λ=0.6 + reranker | **0.875** | **0.705** | First config to beat 0.7 on **both** domains at once |
| `v25_mid_temp_larger` (best single result) | temperature=0.3, n=25 (validated at scale) | **0.957** | 0.598 | Best-ever result, statistically de-risked at larger n |

**Speaker notes:** *(~65s, ~160 words)*
"General knowledge gave us a genuine stress test: hotpotqa needs multi-hop reasoning across several documents, while msmarco is simple single-hop factoid lookup — same pipeline, opposite retrieval needs. Our baseline exposed a serious problem immediately: hotpotqa adherence was 0.393, *below random chance* — our hallucination detector was actively unreliable on multi-hop questions. Across 41 iterations — the widest sweep of any domain on this team — we isolated something important: random seed and sample selection turned out to be a more dominant factor in adherence than almost any single retrieval or generation lever we tuned. `v4` was our first real breakthrough: tuned sentence-window chunking plus a diversity-biased MMR setting pushed hotpotqa to 0.875 while *also* keeping msmarco above 0.7 — the only config to win both domains simultaneously. `v25` then pushed hotpotqa to its best-ever result, 0.957, and crucially validated it at a larger sample size of 25 to rule out lucky sampling."

---

## SLIDE 12 — General Knowledge (Arhan), Slide 2 of 2: Key Findings & Conclusion

**On-slide text:**

**Title:** General Knowledge — When Seed Selection Beats Configuration

**[CHART — combo bar+line, per the recurring pattern, adapted: this domain's headline metric is adherence per sub-domain, not pooled RMSE]**
Grouped bar chart — X-axis: `v0_baseline` → `v4_hotpotqa` → `v25_mid_temp_larger`
Two bar series: Hotpotqa Adherence AUCROC, Msmarco Adherence AUCROC (both 0–1, dashed reference line at 0.5)
*Visual story: hotpotqa bar climbs from below the 0.5 line at baseline, to 0.875, to 0.957; msmarco bar stays consistently strong (0.82 → 0.70 → 0.60), illustrating the real cross-domain tradeoff.*

**Key findings:**
- **Seed/sample selection is the single most dominant factor found in this project** — identical configs at different seeds swung hotpotqa adherence from 0.36 to 0.96, larger than almost any deliberate config change
- **Domain-specific chunking strategy**: sentence-window chunking favors hotpotqa's multi-hop structure; recursive/fixed-size chunking favors msmarco's continuous prose — no single chunking strategy wins both
- **Temperature has an optimal range (0.1–0.4), not a monotonic relationship** — both temperature=0.0 (fully deterministic) and temperature=0.7+ underperformed the 0.3 sweet spot
- **A genuine best-of-both-domains config exists** (`v4`) even though the single-best-hotpotqa config (`v25`) trades away some msmarco performance

**Conclusion:** Two valid recommendations depending on goal — **best balanced dual-domain config: `v4`** (0.875 / 0.705) — **best single-domain ceiling: `v25`** (0.957 hotpotqa, statistically validated at n=25). Either way: **seed control and larger samples matter as much as the config itself.**

**Speaker notes:** *(~65s, ~160 words)*
"This chart shows both bars climbing together at `v4` — proof that a genuine dual-domain win is possible, it just requires the right chunking-plus-MMR combination. But look at `v25`: hotpotqa keeps climbing to its best-ever 0.957, while msmarco gives some of that back, down to 0.598 — a real, visible tradeoff, not noise. The finding we most want this room to remember: across our whole sweep, simply changing the random seed — with *zero* config change — swung hotpotqa adherence between 0.36 and 0.96. That's a bigger swing than almost any deliberate lever we tested, including temperature and chunking. We also found temperature has a genuine sweet spot around 0.3, not a 'lower is always safer' relationship — both fully deterministic generation and high-temperature generation underperformed. So we're presenting two honest recommendations: `v4` if you need one config that works reasonably well on both domains, and `v25` if you're optimizing purely for multi-hop adherence and can validate at a larger sample size."

---

## SLIDE 13 — Key Takeaways (Cross-Domain Synthesis)

**On-slide text:**

**Title:** Four Domains, One Evaluation Discipline

**[CHART — cross-domain comparison, radar or grouped-bar]**
Radar chart, 4 axes (Relevance RMSE inverted-to-score, Utilization RMSE inverted-to-score, Completeness RMSE inverted-to-score, Adherence AUCROC), 4 overlaid series (one per domain, using each domain's assigned accent color from the deck), plotted at each domain's *final adopted config*.

**Final adopted configs, side by side:**

| Domain | Final config | Relevance RMSE ↓ | Utilization RMSE ↓ | Completeness RMSE ↓ | Adherence AUCROC ↑ |
|---|---|---|---|---|---|
| Biomedical | `v8e` | 0.321 | 0.149 | 0.399 | 0.870 |
| Legal | `v19_colleague_hybrid_rich` | 0.297 | 0.060 | 0.552 | 0.810 |
| Financial (FinQA) | `v4` | 0.122 | 0.112 | 0.186 | 0.786 |
| General Knowledge | `v4_hotpotqa` (balanced pick) | — | — | — | 0.875 / 0.705* |

*\*General knowledge reports per-sub-domain adherence rather than a single pooled figure, reflecting its intentional hotpotqa/msmarco asymmetry design.*

**Top 3 takeaways (numbered callout boxes, one icon each):**
1. **Judge/generator independence and MMR-style diversity were the two most consistently powerful levers** — found separately, by separate people, on separate domains
2. **Chunking helps some domains and hurts others — there is no universal RAG recipe.** Every "one-size-fits-all" config we tried eventually broke on at least one domain
3. **Every team independently discovered and had to control for a reproducibility confound** (seed, sample composition, or judge non-determinism) before trusting their own results — this is arguably the single most important shared finding of the whole project

**Visual aid:** Radar chart center-stage, with the 3 numbered takeaway callouts as a sidebar or footer strip, each with a small icon (independence = two separate circles linking, diversity = scattered dots forming a spread, reproducibility = a repeating-loop icon). **Animation:** radar chart's 4 domain overlays fade in one at a time as the speaker names each domain, then the 3 takeaway callouts slide in together as the synthesizing close.

**Speaker notes (whoever leads this slide, or all four briefly):** *(~50s, ~120 words)*
"Stepping back across all four domains: two levers came up as genuinely powerful, independently, in separate domains, by separate people — judge and generator independence, and diversity-aware retrieval like MMR. Second, we want to push back on the idea that there's a single best RAG recipe: chunking helped legal and general knowledge in places, but consistently hurt biomedical, and top-k settings that were optimal for one domain collapsed another. And third — in every single domain, someone on this team ran into a reproducibility problem — an unseeded generator, a lucky sample draw, a non-deterministic judge — and had to control for it before trusting their own numbers. That's arguably the most important finding of this whole project: not any one config, but the discipline of not believing a result until you've ruled out noise."

---

## SLIDE 14 — Limitations & Next Steps

**On-slide text:**

**Title:** What We'd Fix With More Time

**Limitations (shared across teams):**
- **Adherence AUCROC is statistically fragile at small sample sizes** — with only 1–3 true-hallucination examples per 15–20 row sample in several domains, a single row flipping can swing AUCROC by 0.2–0.4
- **Ground truth is not infallible** — the financial track found RAGBench's own reference response contained a real arithmetic error on at least one question, meaning a "wrong" adherence score sometimes reflects a bad reference, not a bad pipeline
- **Judge non-determinism, even at `temperature=0.0`** — the financial track found the same judge call, on byte-identical input, occasionally reached a different verdict
- **No single configuration transfers across all four domains** — every team found at least one lever (chunking, top-k, embedding choice) that helped one domain and hurt another

**Next steps:**
- Scale sample size (n=15–20 → 30+) across all domains for statistically stable adherence estimates
- Judge-prompt refinement targeting the recurring "scaffolding-sentence" leniency inconsistency found independently in the financial and biomedical tracks
- Move adherence from a boolean-per-sentence judgment to a continuous confidence score, reducing AUCROC's sensitivity to single-row flips
- A shared, cross-team judge-calibration study, since 3 of 4 domains found judge choice mattered more than retrieval sophistication

**Visual aid:** Two-column layout — left column "Limitations" under a warning-triangle icon, right column "Next Steps" under a roadmap/arrow icon with 4 sequential milestone dots. **Animation:** left column populates first (paired with the speaker's limitations narration), then the right column's roadmap draws in left-to-right as the speaker pivots to next steps.

**Speaker notes:** *(~45s, ~110 words)*
"We want to be upfront about the limits of what we're presenting. Adherence AUCROC is statistically fragile at these sample sizes — a single misclassified row can swing it by 0.3 or more, and we saw that repeatedly. Ground truth itself isn't infallible either — our financial team actually found an arithmetic error in RAGBench's own reference answer for one question. And judge non-determinism is real, even at zero temperature. Going forward, the highest-value next steps are scaling up sample size, refining the judge prompt around a leniency pattern we found independently in two domains, and moving toward a continuous rather than boolean adherence score."

---

## SLIDE 15 — Questions

**On-slide text:**
> Questions?
> Thank you.
> [Team names] · Capstone Project 2026

**Visual aid:** Minimal, calm closing slide — same four domain icons from the title slide, now shown together/overlapping to signal "one project, four domains," on the neutral frame accent color. Optional: a QR code or contact line if the team wants to share the full write-up.

**Speaker notes:** *(~10s)*
"Thank you — we're happy to take your questions."

---

## Timing Summary

| Slide(s) | Content | Target time |
|---|---|---|
| 0 | Title | 0:15 |
| 1 | Agenda & Team | 0:30 |
| 2 | Problem & Objective | 0:45 |
| 3 | Dataset & Framework | 0:45 |
| 4 | Pipeline Architecture | 0:50 |
| 5–6 | Biomedical | 2:10 |
| 7–8 | Legal | 2:10 |
| 9–10 | Financial | 2:10 |
| 11–12 | General Knowledge | 2:10 |
| 13 | Key Takeaways | 0:50 |
| 14 | Limitations & Next Steps | 0:45 |
| 15 | Questions | 0:10 |
| **Total** | | **~13:35** |

This leaves roughly 1:25 of true open buffer within a 15-minute slot (10 min original target + 5 min buffer), given the added front-matter and closing sections. If a stricter 10-minute *speaking* limit is a hard requirement rather than a soft target, the fastest place to cut is tightening each domain's speaker notes back toward ~45s (drop the methodology-at-a-glance bullet on slide 1 of each domain pair) rather than cutting the new framework/limitations slides, since those are what the professor explicitly asked to see.
