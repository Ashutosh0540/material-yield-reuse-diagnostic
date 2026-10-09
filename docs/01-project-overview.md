# 01 — Project overview

## Purpose

This repository supports an anonymized Forward Deployed Engineer case study. It demonstrates how an open-ended request for AI nesting optimisation can be translated into a measurable discovery question and a small, inspectable decision-support example.

## Audience

Senior FDE and engineering interviewers, fabrication operations stakeholders, and reviewers assessing the reasoning, controls, and boundaries of a proposed industrial workflow.

## Business context and evidence labels

**User-provided case context:** the anonymous structural steel fabrication client expressed interest in AI-powered nesting optimisation. Discovery was described as identifying possible themes in material yield and waste, reusable remnants, drawing revisions, project allocation, yard accessibility, and existing STRUMIS capabilities. These supplied themes are not independently verified and this repository contains no client record or measurement.

**Assumptions and hypotheses:** material attributes, current systems, remnant identity, and operating controls may affect reuse; improving visibility could help. These require validation. See the [assumptions register](../analysis/assumptions-register.md).

## Implemented versus proposed

| Implemented here | Proposed for a future engagement |
|---|---|
| Python CLI reads a JSON requirement and candidates. | Four-week read-only diagnostic with client-approved evidence. |
| Deterministic field checks produce reasoned `eligible`, `ineligible`, or `human_review` results. | Baseline measurement, workflow observation, and validation with domain owners. |
| In-memory approval function requires an explicit approval flag for an eligible result. | Configure existing tools, change process, pilot, or do not build based on evidence. |
| Synthetic data and unit tests. | Any integration, live workflow, or production system. |

## Demonstration success criteria

The demonstration succeeds if a reviewer can reproduce its outputs, see why each candidate receives its status, confirm unknowns do not become approval, and distinguish code behavior from the proposed diagnostic. These are repository criteria, not evidence of business impact.

Continue to [problem and process](02-problem-and-process.md) or return to the [README](../README.md).
