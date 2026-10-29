# Round Agent Instructions

Reusable instruction set for one brainstorm round. The orchestrator passes in: **round + agent ID**, **lens**, **output file path**, and **target count**.

## Rules
1. **No internet.** Don't use web search, web fetch, curl, or any connector/MCP tool. Reason from what you already know. Only read the two files in `solo-income/` and write your output file.
2. **Read `solo-income/ideas.md` in full first.** That's the brief, the card format, and every idea already accepted.
3. **Only add ideas that are actually new.** An idea counts as new only if it differs from every listed idea in at least one of: *approach* (mechanism of value), *resource used*, or *constraint exploited*. A new customer for the same product doesn't count, and neither does a new channel for the same product. In the `Unique:` line, name the closest existing idea and say what differs.
4. **Think wide, then cut.** Generate at least 3x the target as raw candidates, privately. Re-read the brief's resources and constraints at least twice while doing it, and ask of each one: *What does this make cheap, or possible, that wasn't before?* Keep only the strongest, most distinct ones.
5. **Honor the constraints.** Solo, silent validation only, ~$0 budget, first dollar in weeks, ethical and legal. Library databases are licensed: use them for research, never republish their content. Public records that name private individuals can't be the product. Mark regulated areas `Flags: legal review`.
6. **Be concrete.** Name the buyer, the price, the channel, and a silent test with a numeric pass/fail threshold. Prefer channels that already have buyer traffic, so no outreach is needed (marketplaces, app/plugin stores, search, public bid portals).
7. **Today is 2026-10-29.** Use timing: the 1931 public-domain wave on Jan 1, 2027, the holiday season, tax season, spring garden season, the chess calendar, and regulatory deadlines.

## Output
Write **only** idea cards to your output file, in the exact card format from `ideas.md`, using temporary IDs `<ROUND><AGENT>-NN` (e.g. `R2B-03`). No preamble. At the end, add one line: `Lens notes: <one sentence on what this lens surfaced or failed to surface>`.

## Lens pool
Each round gets distinct lenses, and fresh agents get lenses not used before.

| Key | Lens |
|---|---|
| L1 | **Stale money flows.** Public bids, permits, the Federal Register, Indeed postings: where businesses or governments pay humans or legacy vendors for work AI/data now makes cheap. |
| L2 | **Free-asset arbitrage.** Public domain (esp. the 1931 wave), public datasets, the seed library, physical stacks: assets that cost $0 but have buyers once refined. |
| L3 | **Skills + existing builds.** Chess, game dev, propagation, versioned catalogs, agent instructions, the budgeting app: what's sellable now with least new work. |
| L4 | **Local geography.** Butler County and the Cincinnati–Dayton corridor: local industries, institutions, history, logistics, and Ohio-specific rules. |
| L5 | **Constraint as moat.** Channels where buyers find you and no-contact selling is normal; products that sell themselves silently. |
| L6 | **AI-adoption picks and shovels.** Use Economic Index occupation/region patterns: sell to occupations adopting AI fast, or to slow adopters with high pain. |
| L7 | **Timing and regulatory windows.** New rules, compliance deadlines, sunsets, seasonal spikes, anniversaries: windows that open and close. |
| L8 | **Inversions + combinations.** Combine two unrelated resources; reverse the obvious direction (sell to sellers, B2B2C, buyer becomes supplier). |
| L9 | **Gap matrix.** Tabulate existing Tags (customer x mechanism x resource), find empty or thin cells, and fill the most promising ones. |
| L10 | **Contrarian / unsexy.** Boring niches, physical–digital hybrids, tiny data products, ideas a typical brainstorm wouldn't produce. |
| L11 | **Second-order effects.** What does mass AI adoption break or create (new chores, new trust gaps, new waste) that someone will pay to fix? |
| L12 | **Saturation check.** Look for whole directions the list hasn't touched at all. If none remain, say so and add fewer cards. |
