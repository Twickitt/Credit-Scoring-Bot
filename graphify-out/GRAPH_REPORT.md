# Graph Report - Credit-Scoring-Bot  (2026-09-11)

## Corpus Check
- 6 files · ~825 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 19 nodes · 36 edges · 4 communities (2 shown, 1 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d15208f7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- bot.py
- predict.py
- Credit Risk Telegram Bot

## God Nodes (most connected - your core abstractions)
1. `main()` - 6 edges
2. `handle_text()` - 5 edges
3. `handle_csv_file()` - 5 edges
4. `predict_dataframe()` - 5 edges
5. `start()` - 4 edges
6. `help_command()` - 4 edges
7. `features_command()` - 4 edges
8. `prepare_dataframe()` - 4 edges
9. `predict()` - 4 edges
10. `Credit Risk Telegram Bot` - 2 edges

## Surprising Connections (you probably didn't know these)
- `handle_text()` --calls--> `predict()`  [EXTRACTED]
  source/bot.py → source/predict.py
- `handle_csv_file()` --calls--> `predict_dataframe()`  [EXTRACTED]
  source/bot.py → source/predict.py

## Import Cycles
- None detected.

## Communities (4 total, 1 thin omitted)

### Community 3 - "bot.py"
Cohesion: 0.58
Nodes (8): DEFAULT_TYPE, features_command(), handle_csv_file(), handle_text(), help_command(), main(), start(), Update

### Community 5 - "predict.py"
Cohesion: 0.53
Nodes (4): DataFrame, predict(), predict_dataframe(), prepare_dataframe()

## Knowledge Gaps
- **1 isolated node(s):** `Структура проекта`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 4 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `predict_dataframe()` connect `predict.py` to `bot.py`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Why does `handle_csv_file()` connect `bot.py` to `predict.py`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `handle_text()` connect `bot.py` to `predict.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `main()` (e.g. with `features_command()` and `handle_csv_file()`) actually correct?**
  _`main()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Структура проекта` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._