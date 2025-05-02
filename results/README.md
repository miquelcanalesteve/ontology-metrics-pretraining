# README – Results Folder

## Overview

The `results` folder contains the key outputs generated over the full dataset of **1766 ontologies**, including:
- `full_dataset_with_ORI.xlsx` → All ontology metrics + ORI
- `llm_with_ORI.xlsx` → ORI for base and continually pretrained LLM models
- `manual_evaluation.xlsx` → Human-checked error annotations following a detailed evaluation guide

This folder serves as the final evaluation reference after applying all scripts and metrics.

---

## Continual Pretraining Configuration

The LLM (Llama 3.2-1B) was trained under the following main settings:
- Model type: `llama`, causal, training and evaluation enabled
- Training for **2 epochs**, batch size `1`, eval batch size `1`
- Learning rate: `2e-5` with weight decay `1e-1` and decay enabled
- Optimizer: beta1 = `0.9`, beta2 = `0.95`, gradient accumulation: `64`, grad clip: `1.0`
- Steps: max `6145`, no warmup, save every `1000` steps, evaluate every `500` steps, log every step
- Sampling: enabled, precision: bf16-true

These parameters controlled how the LLM was fine-tuned to generate new ontology fragments.

---

## Manual Evaluation Guide

The `manual_evaluation.xlsx` file annotates specific error types found in the generated ontologies, guided by the following categories:

- **Syntactic issues** → Missing or incorrect punctuation (e.g., missing dots, extra brackets)
- **Triplet repetition** → Duplicated triples with identical subject, predicate, object
- **Vocabulary misuse** → Incorrect use of reserved RDF, RDFS, OWL, or XSD terms (e.g., using `owl:Property` instead of `owl:ObjectProperty`)
- **Text repetition** → Redundant comments or repeated literal text adding no new information
- **Semantic redundancy** → Using multiple properties that express the same meaning (e.g., `hasSynonym` vs. `synonym`)
- **Ambiguity** → Unclear or overlapping entities (same label but different subjects, or conflicting definitions)
- **Semantic contradictions** → Logical inconsistencies (e.g., marking the same entity as both a class and a property, or misusing literals/IRIs)

These guidelines ensure a structured manual check of the LLM’s generated ontologies, going beyond what automatic metrics can capture.

---

## Important Note

While the `code/data` folder provides three example ontologies and an `outputs` subfolder holds sample results from these, the ORI and metrics values there **will not match** the full dataset results due to normalization being computed across the complete set of 1766 ontologies.
