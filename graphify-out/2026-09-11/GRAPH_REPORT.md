# Graph Report - Credit-Scoring-Bot  (2026-09-11)

## Corpus Check
- 18 files · ~11,925 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 83 nodes · 89 edges · 16 communities (9 shown, 6 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d15208f7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- What You Must Do When Invoked
- /graphify
- graphify reference: extra exports and benchmark
- bot.py
- graphify reference: query, path, explain
- predict.py
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- Credit Risk Telegram Bot
- CLAUDE.md
- .claude/CLAUDE.md
- extraction-spec.md

## God Nodes (most connected - your core abstractions)
1. `What You Must Do When Invoked` - 12 edges
2. `/graphify` - 10 edges
3. `graphify reference: extra exports and benchmark` - 8 edges
4. `main()` - 6 edges
5. `handle_text()` - 5 edges
6. `handle_csv_file()` - 5 edges
7. `predict_dataframe()` - 5 edges
8. `graphify reference: query, path, explain` - 5 edges
9. `start()` - 4 edges
10. `help_command()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `handle_text()` --calls--> `predict()`  [EXTRACTED]
  source/bot.py → source/predict.py
- `handle_csv_file()` --calls--> `predict_dataframe()`  [EXTRACTED]
  source/bot.py → source/predict.py

## Import Cycles
- None detected.

## Communities (16 total, 6 thin omitted)

### Community 0 - "What You Must Do When Invoked"
Cohesion: 0.13
Nodes (15): Part A - Structural extraction for code files, Part B - Semantic extraction (parallel subagents), Part C - Merge AST + semantic into final extraction, Step 0 - GitHub repos and multi-path merge (only if a URL or several paths), Step 1 - Ensure graphify is installed, Step 2.5 - Video and audio (only if video files detected), Step 2 - Detect files, Step 3 - Extract entities and relationships (+7 more)

### Community 1 - "/graphify"
Cohesion: 0.20
Nodes (9): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Usage (+1 more)

### Community 2 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 3 - "bot.py"
Cohesion: 0.58
Nodes (8): DEFAULT_TYPE, features_command(), handle_csv_file(), handle_text(), help_command(), main(), start(), Update

### Community 4 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 5 - "predict.py"
Cohesion: 0.53
Nodes (4): DataFrame, predict(), predict_dataframe(), prepare_dataframe()

### Community 6 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 7 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 8 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

## Knowledge Gaps
- **44 isolated node(s):** `graphify`, `Usage`, `What graphify is for`, `Step 0 - GitHub repos and multi-path merge (only if a URL or several paths)`, `Step 1 - Ensure graphify is installed` (+39 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 58 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `What You Must Do When Invoked` connect `What You Must Do When Invoked` to `/graphify`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Why does `/graphify` connect `/graphify` to `What You Must Do When Invoked`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `main()` (e.g. with `features_command()` and `handle_csv_file()`) actually correct?**
  _`main()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify`, `Usage`, `What graphify is for` to the rest of the system?**
  _44 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `What You Must Do When Invoked` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._