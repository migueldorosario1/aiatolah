---
layout: ../../../layouts/PostLayout.astro
title: "Alibaba's Qwen3 235B: The Largest Open-Source Model — And It's Chinese"
date: 2026-05-19
category: "Open Source"
lang: "en"
excerpt: "Alibaba's Qwen3 235B-A22B is the largest open-source language model available, outperforming GPT-4o on multiple benchmarks while being freely downloadable and self-hostable."
source: "https://qwenlm.github.io"
heroImage: "/hero/qwen3.png"
---

# Alibaba's Qwen3 235B: The Largest Open-Source Model — And It's Chinese

Alibaba's Qwen team has released Qwen3 235B-A22B, a 235-billion parameter Mixture-of-Experts model that is now the largest freely available open-source language model in the world — and it outperforms OpenAI's GPT-4o on several key benchmarks.

## What 235B-A22B Means

The model name encodes its architecture: 235 billion total parameters, with 22 billion activated per forward pass (A22B). This MoE design means inference is computationally comparable to a 22B dense model, making self-hosting feasible on modern GPU clusters without requiring the largest data centers.

The model achieves state-of-the-art scores on MMLU (multilingual reasoning), HumanEval (code generation), and MATH (mathematical problem solving) — putting it in the same tier as GPT-4o while remaining fully open source.

## A Strategic Move Against Western Dominance

Alibaba's decision to open-source Qwen3 235B is explicitly strategic. By releasing the model weights freely, Qwen aims to:

- Build developer mindshare globally before proprietary competitors lock in customers
- Establish Chinese AI as the default open-source stack for organizations that cannot afford Western API pricing
- Demonstrate that China can lead on both frontier capability and openness simultaneously

## Via API at Commodity Prices

For those who prefer managed inference, Qwen3 235B-A22B is available via Alibaba's DashScope API at $0.22 per million input tokens — making it the cheapest frontier-quality model per token after DeepSeek V3.

For Global South organizations, universities, and governments that cannot afford $3-15/M token pricing from Western providers, Qwen3's combination of open-source availability and cheap managed inference is transformative.

*With information from Alibaba Qwen team.*
