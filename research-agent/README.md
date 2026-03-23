# Research Agent

Production-grade research agent with auto-detection of research types, academic frameworks, and systematic investigation patterns.

## Overview

This skill conducts structured, source-backed research across 5 research types. It applies academic frameworks for rigor and includes root cause analysis patterns for technical investigations.

## Features

- **5 research types** (auto-detected):
  - Exploratory: broad investigation of a new topic
  - Descriptive: detailed characterization of a known topic
  - Explanatory: understanding why something works the way it does
  - Evaluative: comparing options or assessing quality
  - Comparative: side-by-side analysis of alternatives

- **Academic frameworks**:
  - PICO (Population, Intervention, Comparison, Outcome)
  - SPICE (Setting, Perspective, Intervention, Comparison, Evaluation)
  - PECO (Population, Exposure, Comparison, Outcome)
  - GRADE (quality of evidence rating)
  - ReAct (Reasoning + Acting for iterative research)

- **Root cause analysis**:
  - 5 Whys technique
  - Fishbone (Ishikawa) diagrams

- **Research quality**: Source-backed findings, bias awareness, systematic review protocol

## When to Use

- Investigating a new technology or approach
- Comparing tools, frameworks, or architectures
- Understanding why a system behaves a certain way
- Conducting due diligence on a technical decision
- Root cause analysis for bugs or incidents

## Installation

```
/plugin install research-agent
```

## Usage

The skill triggers automatically on research-oriented requests. Examples:

- "Research best practices for real-time multiplayer architecture"
- "Compare RabbitMQ vs Kafka for our use case"
- "Investigate why our API latency increased last week"
- "What are the current approaches to LLM evaluation?"

## License

Apache License 2.0 - See LICENSE.txt
