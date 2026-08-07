---
layout: ../../../layouts/PostLayout.astro
title: 'How to Schedule a Weekly Metrics Report With ChatGPT Work - Insights'
date: 2026-08-07
category: 'YouTube'
lang: "en"
source: 'https://www.youtube.com/watch?v=p_slDAvPjv0'
heroImage: "/hero/youtube-p_slDAvPjv0.jpg"
---

# How to Schedule a Weekly Metrics Report With ChatGPT Work

<div class="youtube-embed" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin: 25px 0; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 8px 32px rgba(0,0,0,0.5);">
  <iframe src="https://www.youtube.com/embed/p_slDAvPjv0" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 12px;"></iframe>
</div>

Here is a detailed technical summary of the video "How to Schedule a Weekly Metrics Report With ChatGPT Work".

### Overview

The video demonstrates a new automation capability within OpenAI’s ecosystem, tentatively named "ChatGPT Work," which enables users to build, refine, and schedule recurring analytical workflows directly from a chat interface. The presenter, a data scientist at OpenAI, shows how this tool transforms a manual 3–4 hour weekly reporting process into an automated, scheduled action that delivers a complete first draft every Thursday morning.

### Key Technical Components

1. **ChatGPT Work Interface**
   - The workflow begins by switching to the "ChatGPT Work" mode, accessible via the desktop app or web client. This appears to be a separate environment or plugin system optimized for persistent, repeatable tasks rather than one-off conversations.

2. **Data Source Integration**
   - The user connects their reporting data stored in **Google Drive**. This suggests direct cloud storage integration, where ChatGPT Work can access spreadsheet files (likely CSV, Sheets, etc.) without manual export/import.

3. **Data Analytics Plugin**
   - A dedicated "data analytics plugin" is installed. This plugin augments ChatGPT’s capabilities specifically for creating better visualizations and reports. It implies enhanced parsing of structured data, chart generation (likely Python-based plotting like matplotlib/seaborn via code interpreter), and narrative analysis.

4. **Configuration Through Examples**
   - The user shares:
     - **KPIs and targets**: Defines what metrics matter (e.g., user growth, retention, feature adoption) and their expected performance thresholds.
     - **A sample report**: Provides a "gold standard" example of the desired output format, tone, and structure. This serves as a few-shot template for the model to mimic.

5. **Iterative Refinement**
   - The system generates an initial report, and the user reviews/adjusts it. This feedback loop tunes the output’s accuracy, commentary style, and chart specifications before the workflow is locked in.

6. **Scheduled Execution Engine**
   - Once satisfied, the user schedules the workflow to run automatically **every Thursday morning**. The video describes this as a "recording workflow," implying that the sequence of actions—data pull, analysis, narrative drafting—is captured and replayed on a cron-like timer.

7. **Automated Analytics Workflow**
   - The full hands-off process:
     1. Pulls the latest weekly KPI data from Google Drive.
     2. Computes week-over-week changes.
     3. Identifies the biggest drivers behind metric movements (variance decomposition, contribution analysis, or similar).
     4. Drafts a "story behind the metrics," translating dry numbers into executive-summary prose.
     5. Updates any embedded charts with fresh data.
     6. The final report is ready and waiting for the user every Thursday morning without any manual trigger.

### Technical Takeaways

- **Architecture**: Likely combines a Code Interpreter backend (for data analysis and plotting) with a scheduling layer that stores workflow definitions and secrets (Google Drive OAuth tokens). The "recording" mechanism probably serializes a sequence of tool calls and model prompts.
- **Automation Scope**: Not just a scripted data pull; the model actively interprets results, isolates key drivers, and writes human-readable narratives—tasks previously requiring subject matter expertise and manual effort.
- **Comparative Advancement**: While Chinese AI platforms like DeepSeek and Qwen push the envelope on open-source LLM reasoning and long-context analysis, and Kimi explores agent-based task decomposition, this video illustrates OpenAI’s tight integration of LLM reasoning with persistent, scheduled automation and third-party data plugins—bringing us closer to an always-on AI analyst rather than a reactive chatbot. Similar to how hardware innovations (like Huawei’s Ascend chips or custom silicon from Biren) accelerate on-device inference, such cloud-based workflow automations offload repetitive analytical labor, enabling professionals to focus on strategic decisions.
