#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_RECEIPTS_PATH = Path(
    os.getenv("AIATOLAH_PUBLICACOES_METRICAS", "agent_data/publicacoes_metricas.jsonl")
)


def agora_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def registrar_publicacao(
    *,
    post_id: str,
    title: str,
    agent: str,
    status: str,
    lang: str = "pt",
    category: str = "",
    stage: str = "publish",
    models: list[str] | None = None,
    tokens_total: int = 0,
    cost_usd: float = 0.0,
    source_name: str = "",
    source_url: str = "",
    duration_seconds: float | None = None,
    receipts_path: Path | str = DEFAULT_RECEIPTS_PATH,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Grava um recibo append-only para cada post do Aiatolah."""

    path = Path(receipts_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    receipt: dict[str, Any] = {
        "site": "aiatolah",
        "post_id": post_id,
        "title": title,
        "published_at": agora_iso(),
        "lang": lang,
        "category": category,
        "agent": agent,
        "stage": stage,
        "models": models or [],
        "tokens_total": int(tokens_total or 0),
        "cost_usd": round(float(cost_usd or 0.0), 6),
        "source_name": source_name,
        "source_url": source_url,
        "status": status,
    }
    if duration_seconds is not None:
        receipt["duration_seconds"] = round(float(duration_seconds), 3)
    if extra:
        receipt["extra"] = extra

    with path.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(receipt, ensure_ascii=False, sort_keys=True) + "\n")

    empurrar_prometheus(receipt)
    return receipt


def empurrar_prometheus(receipt: dict[str, Any]) -> bool:
    """Envia métrica ao Prometheus se o ambiente estiver configurado.

    Falha de Prometheus nunca deve derrubar publicação.
    """

    gateway = os.getenv("AIATOLAH_PROMETHEUS_PUSHGATEWAY", "").strip()
    if not gateway:
        return False

    try:
        from prometheus_client import CollectorRegistry, Counter, Gauge, push_to_gateway
    except Exception:
        return False

    try:
        registry = CollectorRegistry()
        labels = ["site", "agent", "stage", "status", "lang", "category", "post_id"]
        label_values = {
            "site": "aiatolah",
            "agent": str(receipt.get("agent", "")),
            "stage": str(receipt.get("stage", "")),
            "status": str(receipt.get("status", "")),
            "lang": str(receipt.get("lang", "")),
            "category": str(receipt.get("category", "")),
            "post_id": str(receipt.get("post_id", "")),
        }

        post_cost = Gauge(
            "aiatolah_post_custo_usd",
            "Custo estimado em USD por post publicado pelo Aiatolah.",
            labels,
            registry=registry,
        )
        post_tokens = Gauge(
            "aiatolah_post_tokens",
            "Tokens usados por post publicado pelo Aiatolah.",
            labels,
            registry=registry,
        )
        posts_total = Counter(
            "aiatolah_agent_posts_total",
            "Quantidade de posts processados por agente do Aiatolah.",
            labels,
            registry=registry,
        )
        pipeline_seconds = Gauge(
            "aiatolah_pipeline_seconds",
            "Duracao da etapa do pipeline do Aiatolah em segundos.",
            labels,
            registry=registry,
        )

        values = [label_values[name] for name in labels]
        post_cost.labels(*values).set(float(receipt.get("cost_usd") or 0.0))
        post_tokens.labels(*values).set(float(receipt.get("tokens_total") or 0))
        posts_total.labels(*values).inc()
        if "duration_seconds" in receipt:
            pipeline_seconds.labels(*values).set(float(receipt["duration_seconds"]))

        job = os.getenv("AIATOLAH_PROMETHEUS_JOB", "aiatolah")
        instance = os.getenv("AIATOLAH_PROMETHEUS_INSTANCE", "aiatolah_local")
        push_to_gateway(gateway, job=job, registry=registry, grouping_key={"instance": instance})
        return True
    except Exception:
        return False


def iniciar_timer() -> float:
    return time.monotonic()


def segundos_desde(inicio: float) -> float:
    return time.monotonic() - inicio


if __name__ == "__main__":
    registrar_publicacao(
        post_id="smoke-aiatolah",
        title="Smoke de métricas do Aiatolah",
        agent="aiatolah_smoke",
        status="dry_run",
        models=[],
        tokens_total=0,
        cost_usd=0.0,
        source_name="local",
        source_url="",
        duration_seconds=0.0,
    )
    print("OK: recibo de smoke registrado.")
