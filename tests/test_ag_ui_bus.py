"""Tests for the AG-UI event bus (a2_mo_composites.ag_ui_bus)."""

from __future__ import annotations

import asyncio
import json

import pytest

from ass_ade.a2_mo_composites.ag_ui_bus import (
    AGUIBus,
    AGUIEvent,
    AGUIEventType,
    get_bus,
    reset_bus,
)


def test_event_to_sse_is_json_lines() -> None:
    ev = AGUIEvent(type=AGUIEventType.TEXT_MESSAGE_CONTENT, data={"delta": "hi"}, run_id="r1")
    sse = ev.to_sse()
    assert sse.startswith("data: ")
    assert sse.endswith("\n\n")
    payload = json.loads(sse[len("data: "):-2])
    assert payload["type"] == "TEXT_MESSAGE_CONTENT"
    assert payload["data"]["delta"] == "hi"
    assert payload["runId"] == "r1"


def test_publish_appends_to_history() -> None:
    bus = AGUIBus(buffer_size=3)
    bus.emit(AGUIEventType.RUN_STARTED, {"input": "a"})
    bus.emit(AGUIEventType.RUN_STARTED, {"input": "b"})
    assert len(bus.history()) == 2


def test_history_ring_buffer_caps() -> None:
    bus = AGUIBus(buffer_size=2)
    for i in range(5):
        bus.emit(AGUIEventType.TEXT_MESSAGE_CONTENT, {"delta": str(i)})
    items = bus.history()
    assert len(items) == 2
    assert [i["data"]["delta"] for i in items] == ["3", "4"]


def test_set_state_emits_delta_and_nests_path() -> None:
    bus = AGUIBus()
    bus.set_state("memory.anchors.prod", "always run tests")
    assert bus.snapshot() == {"memory": {"anchors": {"prod": "always run tests"}}}
    last = bus.history()[-1]
    assert last["type"] == "STATE_DELTA"
    assert last["data"]["path"] == "memory.anchors.prod"


def test_emit_widget_uses_widget_card_type() -> None:
    bus = AGUIBus()
    ev = bus.emit_widget("scout_report", {"repo": "/tmp/x"}, run_id="r7")
    assert ev.type == AGUIEventType.WIDGET_CARD
    assert ev.data["kind"] == "scout_report"
    assert ev.data["payload"]["repo"] == "/tmp/x"
    assert ev.run_id == "r7"


def test_get_bus_singleton() -> None:
    reset_bus()
    a = get_bus()
    b = get_bus()
    assert a is b
    reset_bus()


@pytest.mark.asyncio
async def test_subscribe_receives_published_events() -> None:
    bus = AGUIBus()

    received: list[AGUIEvent] = []

    async def consumer() -> None:
        async for ev in bus.subscribe():
            received.append(ev)
            if len(received) == 2:
                break

    task = asyncio.create_task(consumer())
    await asyncio.sleep(0.05)
    bus.emit(AGUIEventType.RUN_STARTED, {"input": "hi"})
    bus.emit(AGUIEventType.RUN_FINISHED, {})
    await asyncio.wait_for(task, timeout=2.0)

    assert [e.type for e in received] == [AGUIEventType.RUN_STARTED, AGUIEventType.RUN_FINISHED]


@pytest.mark.asyncio
async def test_subscribe_replay_yields_history_first() -> None:
    bus = AGUIBus()
    bus.emit(AGUIEventType.TEXT_MESSAGE_CONTENT, {"delta": "old"})

    received: list[AGUIEvent] = []

    async def consumer() -> None:
        async for ev in bus.subscribe(replay=1):
            received.append(ev)
            if len(received) == 2:
                break

    task = asyncio.create_task(consumer())
    await asyncio.sleep(0.05)
    bus.emit(AGUIEventType.TEXT_MESSAGE_CONTENT, {"delta": "new"})
    await asyncio.wait_for(task, timeout=2.0)

    assert received[0].data["delta"] == "old"
    assert received[1].data["delta"] == "new"
