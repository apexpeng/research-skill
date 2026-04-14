# Quality Baseline

## Overview

This document defines quantitative and qualitative thresholds for paper quality assessment across all workflow stages. Inspired by ARIS's score progression tracking (5→8.5/10).

## Score Framework

### Overall Score (0-10)

| Score | Label | Interpretation | Action |
|-------|-------|----------------|--------|
| 0-3 | Reject-level | Major flaws in evidence, logic, or methodology | Return to paper-draft |
| 4-5 | Borderline | Some merit but significant gaps | paper-review-loop required |
| 6-7 | Acceptable | Meets basic standards, minor revisions needed | Proceed with fixes |
| 8-9 | Strong | Publication quality, minor polish | paper-figure/supplement |
| 10 | Top-tier | Ready for top venue | paper-export-en |

### Dimension Scores

Each review produces four dimension scores:

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Evidence Chain | 30% | Claim-evidence alignment, experimental design |
| Logical Rigor | 30% | Reasoning chains, control variables, limitations |
| Reviewer Risk | 25% | Overclaiming, method vulnerabilities, citations |
| Structural Coherence | 15% | Section flow, figure references, supplements |

### Minimum Passing Thresholds

| Stage | Minimum Score | Notes |
|-------|---------------|-------|
| paper-intake | N/A | No scoring, only completeness check |
| paper-architecture | N/A | No scoring, only outline coverage check |
| paper-draft | 4/10 | Below this → return to architecture |
| paper-review-loop | 6/10 | Below this → keep iterating |
| paper-figure | N/A | Figure-text alignment check only |
| paper-supplement | N/A | Completeness + non-duplication check |
| paper-export-en | 8/10 | Format compliance + content quality |

## Evidence Chain Checklist

For each claim in `claims_evidence_matrix.md`, verify:

- [ ] **Direct evidence**: Experiment directly tests the claim
- [ ] **Statistical validity**: Sample size, p-values, confidence intervals reported
- [ ] **Control baseline**: Comparison to appropriate baselines
- [ ] **No correlation=causation**: Claims avoid causal language for correlational findings
- [ ] **Effect size reported**: Not just statistical significance

## Logic Chain Checklist

For each reasoning step in the narrative:

- [ ] **Premise stated**: What assumptions are made
- [ ] **Inference valid**: Logical connection between premise and claim
- [ ] **Alternative considered**: Have alternatives been ruled out
- [ ] **Limitation acknowledged**: What weakens the inference

## Reviewer Risk Checklist

Common reviewer objections to pre-emptively address:

- [ ] **"This was already done in [Paper X]"** → Novelty check passed
- [ ] **"The baseline is unfair"** → All major baselines compared
- [ ] **"The claim is overstated"** → Hedging language used appropriately
- [ ] **"Why this method and not [Alternative]?"** → Ablation studies included
- [ ] **"What about [Edge Case]?"** → Limitations section addresses scope

## Structural Completeness Checklist

| Section | Required? | Min Length | Check |
|---------|-----------|------------|-------|
| Abstract | Yes | 150-250 words | Can standalone convey contribution |
| Introduction | Yes | 0.5-1 page | States problem, gap, contribution |
| Related Work | Yes | 0.5-1 page | Covers key citations, positions work |
| Methods | Yes | 1-2 pages | Sufficient detail to reproduce |
| Experiments | Yes | 1-2 pages | Fair comparisons, sufficient baselines |
| Conclusion | Yes | 0.25-0.5 page | Summarizes, doesn't overclaim |

## Figure Quality Checklist

For each figure in `figure_draft_*.md`:

- [ ] **Caption self-contained**: Can understand figure without reading text
- [ ] **Axis labels readable**: Units, ranges, tick marks present
- [ ] **Color accessibility**: Distinguishable in grayscale
- [ ] **Statistical annotation**: Error bars, significance markers present
- [ ] **Reference in text**: At least one citation in body

## Supplement Completeness Checklist

For each supplement item:

- [ ] **Not duplicated in main text**: Content is truly supplementary
- [ ] **Referenced in main text**: At least one citation
- [ ] **Self-contained**: Can be understood without main paper
- [ ] **Properly formatted**: Tables/figures meet venue guidelines

## Score Progression Tracking

Maintain `review_scores.json` in project root:

```json
{
  "project_key": "...",
  "rounds": [
    {"round": 0, "overall": 5.0, "evidence": 4.5, "logic": 5.0, "reviewer_risk": 5.5, "structure": 5.0, "date": "2026-04-10"},
    {"round": 1, "overall": 6.5, "evidence": 6.0, "logic": 6.5, "reviewer_risk": 7.0, "structure": 6.0, "date": "2026-04-11"}
  ],
  "threshold": 6.0,
  "status": "passed"
}
```

**Stagnation Rule**: If score improvement < 0.3 for 2 consecutive rounds → flag for human intervention.

## Adaptive Thresholds

For complex projects (theory papers, multi-modal, etc.):

- Evidence Chain weight may increase to 40%
- Structural Coherence weight may decrease to 10%
- Additional "Theoretical Soundness" dimension (0-10) added

Configure via `ADAPTIVE_WEIGHTS=true` in project config.
