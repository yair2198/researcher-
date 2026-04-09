# Deep Internet Research Workflow

## Objective
Conduct thorough, multi-pass internet research on any given topic and produce a comprehensive, well-sourced, actionable report in Hebrew. The research must be deep enough that Claude can later ACT on the findings without re-researching.

## Required Inputs
- **Topic/question** from the user (passed as `$ARGUMENTS` or asked directly)
- **Depth** is always comprehensive unless user explicitly requests otherwise

## Output Format
- Hebrew text with structured markdown
- Every claim linked to its source
- Saved to `research/[topic-slug].md` for future use

---

## Phase 0: Knowledge Base Check (Auto-detect)

Before doing ANY research, check if prior work exists on this topic.

1. Run `python tools/research_utils.py list` to see all existing research topics
2. Run `python tools/research_utils.py find "[topic]"` to search for related research
3. **If EXACT match found:**
   - Read the existing research file from `research/[slug].md`
   - Present the executive summary to the user in Hebrew
   - Show the open questions from previous sessions
   - Tell the user: "Found existing research from [date]. Building on it."
   - Proceed to Phase 1 with constraint: **ONLY search for NEW information**
   - Check the Research Log section to avoid repeating previous queries
4. **If RELATED topics found:**
   - Present the list: "Found related research: [topics]. Want to combine or research separately?"
   - Load relevant research as background context
5. **If NO match found:**
   - Proceed normally as fresh research
6. **Read `workflows/research_lessons.md`** before proceeding — apply any global lessons learned from past research sessions

---

## Phase 1: Scoping & Decomposition

### 1.1 Parse the Research Question
- Identify the **core topic** and 3-5 **subtopics** to investigate
- Classify the research TYPE:
  - `factual` — verifiable facts, data, definitions
  - `comparative` — comparing options, alternatives, trade-offs
  - `trend` — evolution over time, future projections
  - `technical` — how something works, implementation details
  - `market` — market size, players, competition, pricing
  - `opinion` — public sentiment, expert opinions, debates
  - `strategy` — actionable methods, frameworks, step-by-step approaches

### 1.2 Define Research Axes
Create 3-5 angles to investigate. Example for "investing in the stock market":
- Axis 1: Core strategies and approaches
- Axis 2: Risk management and common mistakes
- Axis 3: Tools, platforms, and practical setup
- Axis 4: Expert consensus vs. contrarian views
- Axis 5: Israeli/local context and regulations

### 1.3 Set Success Criteria
Define what a "complete" answer looks like. Write it down before searching.
Example: "Research is complete when we have: 3+ validated strategies with pros/cons, risk factors documented, practical getting-started steps, and Israeli-specific considerations."

### 1.4 Clarify if Needed
If the topic is ambiguous, ask the user **ONE** clarifying question before proceeding. Don't guess — one question saves three correction rounds.

---

## Phase 2: Broad Discovery (Wide Net)

### 2.1 Run 5-7 Varied WebSearch Queries
Use different formulations to maximize coverage:

| Query Type | Pattern | Example |
|------------|---------|---------|
| Direct | `[topic]` | `stock market investing strategies` |
| Contextual | `[topic] analysis [current year]` | `stock market investing analysis 2026` |
| Expert | `[topic] expert opinion research` | `investing expert opinion research` |
| Data | `[topic] statistics data report` | `stock market returns statistics data` |
| Critical | `[topic] criticism challenges problems` | `stock investing risks common mistakes` |
| Alternative | `[topic] alternatives comparison` | `stock vs ETF vs bonds comparison` |
| Hebrew | `[topic in Hebrew]` | `השקעה בבורסה אסטרטגיות` |

### 2.2 Map the Information Landscape
After the initial searches:
- Identify the **top 10-15 most promising URLs**
- Categorize sources: academic, news, industry, government, blog, forum
- Note recurring themes and key terminology
- Identify the most-cited experts and institutions

### 2.3 Record Search Results
Keep a mental log of:
- Which queries returned the best results
- Which source types dominate for this topic
- What gaps are already visible

---

## Phase 3: Deep Investigation

### 3.1 Deep-Read Top Sources (WebFetch)
Use WebFetch on the **top 8-12 most authoritative sources** from Phase 2.

For each source, extract:
- **Key claims** with supporting evidence
- **Data points** and statistics (with dates — freshness matters)
- **Expert quotes** and their affiliations
- **Methodology** (if it's a study or report)
- **Publication date** — flag anything older than 2 years

### 3.2 Targeted Follow-up Searches
Run 5-8 additional WebSearch queries for:
- Specific claims that need verification
- Primary sources behind secondary reports (e.g., if a blog cites a study, find the study)
- Counter-arguments and alternative viewpoints
- Most recent developments (add "2025" or "2026" to queries)
- Specific subtopics that emerged as important

### 3.3 Build Source Reliability Assessment
For each major source, mentally rate:
- **Tier 1:** Peer-reviewed research, government data, official reports, primary sources
- **Tier 2:** Major news organizations, established industry publications, recognized expert analysis
- **Tier 3:** Blogs, forums, social media (useful for leads and sentiment, not as primary evidence)

---

## Phase 3.5: Social Media & Community Intelligence

### 3.5.1 Platform-Specific Searches
Run targeted searches on social platforms:

| Platform | Query Pattern | Looking For |
|----------|--------------|-------------|
| Reddit | `site:reddit.com [topic]` | User experiences, detailed discussions, AMAs |
| X/Twitter | `site:x.com [topic]` | Expert opinions, breaking news, public sentiment |
| LinkedIn | `site:linkedin.com [topic]` | Professional insights, industry perspectives |
| YouTube | `site:youtube.com [topic]` | Expert talks, tutorials, interviews |
| HackerNews | `site:news.ycombinator.com [topic]` | Tech-savvy perspectives, startup insights |
| Quora | `site:quora.com [topic]` | Expert answers, diverse perspectives |

Run 3-5 of these searches (choose the most relevant platforms for the topic).

### 3.5.2 Deep-Read Community Content
Use WebFetch on the **top 3-5 most insightful threads/discussions**.

Extract:
- **Dominant sentiment** — what do most people think/feel?
- **Expert voices** — any verified experts contributing?
- **Real-world experiences** — success stories, failures, practical tips
- **Emerging trends** — things not yet in mainstream media
- **Controversies** — what are people arguing about?

### 3.5.3 Label Community Findings
All social media findings MUST be clearly labeled as "community perspective" in the final report. Never present social media opinions as established facts.

---

## Phase 4: Verification & Triangulation

### 4.1 Cross-Reference Claims
For every factual claim in the research:
- **2+ independent sources** → mark as "confirmed"
- **1 source only** → mark as "reported by [source name]"
- **Sources conflict** → present both sides with source quality assessment

### 4.2 Check for Bias Signals
For each major source, evaluate:
- **Recency:** Is this current information?
- **Authority:** Who published this and what are their credentials?
- **Bias:** Does the source have a financial or ideological agenda?
- **Corroboration:** Do independent sources confirm this?

### 4.3 Fill Gaps
- Review findings against the success criteria from Phase 1
- List specific gaps: missing data, unverified claims, unexplored angles
- Run 2-4 additional targeted searches to fill critical gaps
- If a gap cannot be filled, note it transparently in "Open Questions"

---

## Phase 5: Synthesis & Critical Analysis

### 5.1 Structure Findings
Organize by importance (inverted pyramid — most important first):
1. Executive Summary (3-5 dense sentences)
2. Key Facts & Data (bullet list with sources)
3. Strategy / Framework / How-To (actionable knowledge)
4. Important Nuances & Warnings
5. Social & Community Insights
6. Open Questions

### 5.2 Apply Confidence Levels
Categorize every finding:
- **Confirmed:** Multiple independent sources agree
- **Likely true:** Reported by credible source, not contradicted
- **Uncertain:** Conflicting evidence or insufficient data
- **Open question:** Could not be resolved — needs further research

### 5.3 Make It Actionable
The Strategy / Framework section must be detailed enough that Claude (or the user) can **execute** the knowledge without re-researching. Include:
- Step-by-step instructions where applicable
- Specific tools, platforms, or resources mentioned
- Decision criteria for choosing between options
- Common pitfalls and how to avoid them

---

## Phase 6: Delivery & Persistence

### 6.1 Present Report
- Write the full report in **Hebrew**
- Use structured markdown with clear headers
- Every claim includes a clickable source link
- End with a "Sources" table organized by relevance and tier

### 6.2 Save to Knowledge Base
Run `python tools/research_utils.py save "[topic]"` or write directly to `research/[slug].md` following this structure:

```markdown
# [Topic Title]
> Last updated: [date] | Sessions: [n] | Status: actionable

## Executive Summary
[3-5 dense sentences]

## Key Facts & Data
- [Fact] (Source: [title](url))

## Strategy / Framework / How-To
### Step 1: ...
### Step 2: ...

## Important Nuances & Warnings
[Edge cases, common mistakes, counter-arguments]

## Social & Community Insights
[Community perspective — labeled as such]

## Open Questions
- [ ] [Unresolved question]

## Sources
| # | Title | URL | Type | Tier | Key Contribution |
|---|-------|-----|------|------|-----------------|

## Lessons Learned
- [Date]: [What was learned]

## Research Log
| Date | Type | Queries Used | Findings Added |
|------|------|-------------|----------------|
```

### 6.3 For Continuation Sessions
If this was a continuation of existing research:
- Merge new findings into the existing file (don't overwrite)
- Update the executive summary to reflect new information
- Add a new entry to the Research Log
- Highlight what's NEW vs. what was already known

### 6.4 Post-Research Learning
After completing the report:
- Record what queries worked best in the Research Log
- Note any source reliability insights
- If anything went wrong, add to Lessons Learned section
- Update `workflows/research_lessons.md` with any cross-topic insights
- Ask the user: "Is there anything to correct or areas you want me to dig deeper?"

---

## Edge Cases

| Situation | Action |
|-----------|--------|
| Topic too broad | Ask user to narrow OR default to top-level overview with offer to deep-dive on subtopics |
| Topic too narrow/obscure | Report what was found, note limitations, suggest adjacent topics |
| Paywalled content | Note the paywall, extract what's available from snippets, look for alternative free sources |
| Non-English sources | Include if relevant, translate key findings to Hebrew |
| Contradictory information | Present both sides with source quality assessment, let user decide |
| User says "that's wrong" | Correct the finding, record in Lessons Learned, update research_lessons.md if systemic |

---

## Guardrails

- **Max ~25 WebSearch calls** per session (including social media searches)
- **Max ~15 WebFetch calls** per session
- **Always ask** before exceeding these limits
- If research is taking too long, **present interim findings** and ask if user wants to continue
- **Never present social media opinions as facts** — always label the source type
- **Always check publication dates** — flag anything older than 2 years for time-sensitive topics
