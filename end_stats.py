"""End-of-run statistics screen for the OOTxMM Archipelago client.

Computes a summary for any OOTxMM goal (Ganon, Majora, Both, Any, Triforce Hunt, Triforce Quest),
formats a plain-text summary for the client log / clipboard, and renders a dedicated "End Stats"
tab in Archipelago's Kivy GUI (used by both BizHawk Client and OOTxMM Dolphin Client).
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
import logging
import time
from typing import TYPE_CHECKING, Any

from . import items, locations, ootxmm_staticdata

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")

# Reverse lookups built once from static metadata.
LOCATION_ID_TO_NAME: dict[int, str] = {
    loc_id: name for name, loc_id in locations.LOCATION_NAME_TO_ID.items()
}
ITEM_ID_TO_DATA: dict[int, items.OOTxMMItemData] = {
    item.id: item for item in items.OOTxMMItemList
}
CHECK_INFO: dict[str, list[Any]] = ootxmm_staticdata.OOTxMMCheckInfo["checks"]

GOAL_LABELS: dict[str, str] = {
    "ganon": "Defeat Ganon (OoT)",
    "majora": "Defeat Majora (MM)",
    "both": "Defeat Ganon & Majora",
    "any": "Defeat Ganon or Majora",
    "triforce": "Triforce Hunt",
    "triforce3": "Triforce Quest (3 Aspects)",
}

CHECK_TYPE_LABELS: dict[str, str] = {
    "chest": "Chests",
    "npc": "NPCs & Rewards",
    "gs": "Gold Skulltulas",
    "sf": "Stray Fairies",
    "shop": "Shops",
    "scrub": "Business Scrubs",
    "cow": "Cows",
    "fish": "Fishing Pond",
    "heart": "Freestanding Hearts",
    "rupee": "Freestanding Rupees",
    "collectible": "Collectibles",
    "sr": "Silver Rupees",
    "pot": "Pots",
    "grass": "Grass",
    "crate": "Crates",
    "barrel": "Barrels",
    "rock": "Rocks",
    "boulder": "Boulders",
    "boulder-red": "Red Boulders",
    "boulder-silver": "Silver Boulders",
    "tree": "Trees",
    "bush": "Bushes",
    "soil": "Soft Soil",
    "hive": "Beehives",
    "snowball": "Snowballs",
    "icicle": "Icicles",
    "redice": "Red Ice",
    "wonder": "Wonder Items",
    "fairy": "Fairies",
    "fairy-spot": "Fairy Spots",
    "butterfly": "Butterflies",
    "gossip": "Gossip Stones",
    "gossip-big": "Big Gossip Stones",
}

FLAG_PROGRESSION = 0b001
FLAG_USEFUL = 0b010
FLAG_TRAP = 0b100

END_STATS_TAB_TITLE = "End Stats"


@dataclass
class CheckBucket:
    checked: int = 0
    total: int = 0

    @property
    def percent(self) -> float:
        return (self.checked * 100.0 / self.total) if self.total else 0.0


@dataclass
class SenderStat:
    name: str
    total: int
    progression: int
    traps: int


@dataclass
class EndStats:
    player_name: str
    seed_name: str
    goal_key: str
    goal_label: str
    goal_detail: str
    item_pool: str
    rank_title: str
    overall: CheckBucket
    oot: CheckBucket
    mm: CheckBucket
    dungeons: CheckBucket
    overworld: CheckBucket
    bosses_defeated: list[str]
    boss_order: list[str]
    triforce_collected: int = 0
    triforce_required: int = 0
    triforce_local: int = 0
    triforce_remote: int = 0
    triforce_aspects: dict[str, bool] = field(default_factory=dict)
    items_received_total: int = 0
    items_delivered: int = 0
    items_progression: int = 0
    items_useful: int = 0
    items_filler: int = 0
    items_trap: int = 0
    items_oot: int = 0
    items_mm: int = 0
    items_shared: int = 0
    top_senders: list[SenderStat] = field(default_factory=list)
    top_trickster: SenderStat | None = None
    top_check_types: list[tuple[str, CheckBucket]] = field(default_factory=list)
    completed_dungeons: list[str] = field(default_factory=list)
    top_scenes: list[tuple[str, CheckBucket]] = field(default_factory=list)
    elapsed_seconds: float | None = None
    active_seconds: float | None = None
    game_switches: int = 0
    checks_per_hour: float | None = None


def format_duration(seconds: float | None) -> str:
    if seconds is None or seconds < 0:
        return "--"
    total = int(round(seconds))
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours}h {minutes:02d}m {secs:02d}s"
    if minutes:
        return f"{minutes}m {secs:02d}s"
    return f"{secs}s"


def format_scene_name(scene_id: str) -> str:
    prefix = ""
    rest = scene_id
    if scene_id.startswith("OOT_"):
        prefix = "OoT "
        rest = scene_id[4:]
    elif scene_id.startswith("MM_"):
        prefix = "MM "
        rest = scene_id[3:]
    words = rest.replace("_", " ").title()
    return f"{prefix}{words}"


def _pick_rank(overall: CheckBucket, goal_key: str, item_pool: str, traps: int) -> str:
    pct = overall.percent
    if overall.total > 0 and overall.checked >= overall.total:
        return "Legend of Two Worlds (100%)"
    if item_pool == "barren":
        return "Survivor of the Barren Realm"
    if traps >= 10:
        return "Trap-Hardened Hero"
    if goal_key in ("triforce", "triforce3") and pct < 40.0:
        return "Golden Relic Hunter"
    if pct >= 85.0:
        return "Master of Time & Masks"
    if pct >= 65.0:
        return "Hero of Two Worlds"
    if pct >= 40.0:
        return "Champion of Hyrule & Termina"
    return "Swift Hero of Destiny"


def _boss_display(event: str) -> str:
    if event == "OOT_GANON":
        return "Ganon"
    if event == "MM_MAJORA":
        return "Majora"
    return event


def collect_stats(
    ctx: "BizHawkClientContext",
    goals: set[str],
    last_query: int | None = None,
    run_stats: dict[str, Any] | None = None,
) -> EndStats:
    """Gather all end-of-run statistics from Archipelago context and client state."""
    slot_data = getattr(ctx, "slot_data", None) or {}
    settings = slot_data.get("settings", {})
    goal_key = str(settings.get("goal") or "both")
    goal_label = GOAL_LABELS.get(goal_key, goal_key.replace("_", " ").title())
    item_pool = str(settings.get("itemPool") or "normal")

    slot = getattr(ctx, "slot", None)
    player_names = getattr(ctx, "player_names", None) or {}
    player_name = player_names.get(slot, f"Player {slot}" if slot is not None else "Hero")
    seed_name = str(getattr(ctx, "server_seed_name", None) or "Unknown")

    checked_ids: set[int] = set(getattr(ctx, "checked_locations", set()) or set())
    missing_ids: set[int] = set(getattr(ctx, "missing_locations", set()) or set())
    all_ids = checked_ids | missing_ids

    overall = CheckBucket(checked=len(checked_ids), total=len(all_ids))
    oot = CheckBucket()
    mm = CheckBucket()
    dungeons = CheckBucket()
    overworld = CheckBucket()
    by_type: dict[str, CheckBucket] = {}
    by_scene: dict[str, CheckBucket] = {}
    dungeon_scenes: dict[str, CheckBucket] = {}

    for loc_id in all_ids:
        is_checked = loc_id in checked_ids
        name = LOCATION_ID_TO_NAME.get(loc_id, "")
        if name.startswith("OOT "):
            oot.total += 1
            if is_checked:
                oot.checked += 1
        elif name.startswith("MM "):
            mm.total += 1
            if is_checked:
                mm.checked += 1

        info = CHECK_INFO.get(name)
        if info:
            check_type, scene, is_dungeon = info[0], info[1], bool(info[2])
            bucket = dungeons if is_dungeon else overworld
            bucket.total += 1
            if is_checked:
                bucket.checked += 1

            tb = by_type.setdefault(check_type, CheckBucket())
            tb.total += 1
            if is_checked:
                tb.checked += 1

            sb = by_scene.setdefault(scene, CheckBucket())
            sb.total += 1
            if is_checked:
                sb.checked += 1

            if is_dungeon:
                db = dungeon_scenes.setdefault(scene, CheckBucket())
                db.total += 1
                if is_checked:
                    db.checked += 1

    # Items received breakdown
    received = list(getattr(ctx, "items_received", []) or [])
    items_received_total = len(received)
    items_delivered = min(last_query, items_received_total) if last_query is not None else items_received_total

    items_progression = 0
    items_useful = 0
    items_filler = 0
    items_trap = 0
    items_oot = 0
    items_mm = 0
    items_shared = 0

    sender_total: Counter[int] = Counter()
    sender_prog: Counter[int] = Counter()
    sender_traps: Counter[int] = Counter()

    for net_item in received:
        flags = getattr(net_item, "flags", 0) or 0
        if flags & FLAG_TRAP:
            items_trap += 1
        elif flags & FLAG_PROGRESSION:
            items_progression += 1
        elif flags & FLAG_USEFUL:
            items_useful += 1
        else:
            items_filler += 1

        item_data = ITEM_ID_TO_DATA.get(net_item.item)
        if item_data is not None:
            sym = item_data.symbolic_id
            if sym.startswith("OOT_"):
                items_oot += 1
            elif sym.startswith("MM_"):
                items_mm += 1
            elif sym.startswith("SHARED_"):
                items_shared += 1

        sender = getattr(net_item, "player", None)
        if sender is not None and sender != slot and sender > 0:
            sender_total[sender] += 1
            if flags & FLAG_PROGRESSION:
                sender_prog[sender] += 1
            if flags & FLAG_TRAP:
                sender_traps[sender] += 1

    top_senders = [
        SenderStat(
            name=player_names.get(sender, f"Player {sender}"),
            total=count,
            progression=sender_prog[sender],
            traps=sender_traps[sender],
        )
        for sender, count in sorted(
            sender_total.items(),
            key=lambda kv: (-kv[1], -sender_prog[kv[0]], player_names.get(kv[0], "")),
        )[:5]
    ]

    top_trickster: SenderStat | None = None
    if sender_traps:
        trick_id, trick_count = max(
            sender_traps.items(),
            key=lambda kv: (kv[1], sender_total[kv[0]]),
        )
        top_trickster = SenderStat(
            name=player_names.get(trick_id, f"Player {trick_id}"),
            total=sender_total[trick_id],
            progression=sender_prog[trick_id],
            traps=trick_count,
        )

    # Goal-specific details
    ids = ootxmm_staticdata.OOTxMMItemIDs
    triforce_collected = 0
    triforce_required = 0
    triforce_local = 0
    triforce_remote = 0
    triforce_aspects: dict[str, bool] = {}

    run = run_stats or {}
    raw_order = [b for b in run.get("boss_order", []) if b in goals]
    for b in sorted(goals):
        if b not in raw_order:
            raw_order.append(b)
    boss_order = [_boss_display(b) for b in raw_order]
    bosses_defeated = [_boss_display(b) for b in ("OOT_GANON", "MM_MAJORA") if b in goals]

    if goal_key == "triforce":
        piece = ids["SHARED_TRIFORCE"]
        local_map = slot_data.get("local_triforce", {})
        triforce_local = sum(
            1 for loc, item_id in local_map.items()
            if int(loc) in checked_ids and item_id == piece
        )
        triforce_remote = sum(1 for item in received[:items_delivered] if item.item == piece)
        triforce_collected = triforce_local + triforce_remote
        triforce_required = int(settings.get("triforceGoal", 0))
        pool_pieces = int(settings.get("triforcePieces", triforce_required))
        goal_detail = (
            f"{triforce_collected}/{triforce_required} Triforce Pieces collected "
            f"({triforce_local} local, {triforce_remote} received; {pool_pieces} in pool)"
        )
    elif goal_key == "triforce3":
        local_map = slot_data.get("local_triforce", {})
        local_ids = {item_id for loc, item_id in local_map.items() if int(loc) in checked_ids}
        remote_ids = {item.item for item in received[:items_delivered]}
        owned = local_ids | remote_ids
        for aspect in ("POWER", "COURAGE", "WISDOM"):
            triforce_aspects[aspect.title()] = ids["SHARED_TRIFORCE_" + aspect] in owned
        triforce_collected = sum(triforce_aspects.values())
        triforce_required = 3
        parts = [f"{name}: {'Yes' if have else 'No'}" for name, have in triforce_aspects.items()]
        goal_detail = " | ".join(parts)
    elif goal_key == "both":
        order_text = " -> ".join(boss_order) if boss_order else "None"
        goal_detail = f"Defeated: {order_text}"
    elif goal_key == "any":
        who = ", ".join(bosses_defeated) if bosses_defeated else "Completed"
        goal_detail = f"Cleared via: {who}"
    elif goal_key == "ganon":
        goal_detail = "Ganon defeated in Ocarina of Time"
    elif goal_key == "majora":
        goal_detail = "Majora defeated in Majora's Mask"
    else:
        goal_detail = "Goal reached"

    # Top check types (show types with at least 1 checked, ordered by checked count)
    top_check_types = [
        (CHECK_TYPE_LABELS.get(kind, kind.replace("-", " ").title()), bucket)
        for kind, bucket in sorted(
            by_type.items(),
            key=lambda kv: (-kv[1].checked, -kv[1].total, kv[0]),
        )
        if bucket.checked > 0
    ][:6]

    completed_dungeons = [
        format_scene_name(scene)
        for scene, bucket in sorted(dungeon_scenes.items())
        if bucket.total > 0 and bucket.checked >= bucket.total
    ]

    top_scenes = [
        (format_scene_name(scene), bucket)
        for scene, bucket in sorted(
            by_scene.items(),
            key=lambda kv: (-kv[1].checked, -kv[1].percent, kv[0]),
        )
        if bucket.checked > 0
    ][:5]

    # Timing & telemetry
    started_at = run.get("started_at")
    finished_at = run.get("finished_at")
    elapsed_seconds: float | None = None
    if isinstance(started_at, (int, float)) and isinstance(finished_at, (int, float)) and finished_at >= started_at:
        elapsed_seconds = float(finished_at - started_at)
    elif isinstance(started_at, (int, float)):
        elapsed_seconds = max(0.0, time.time() - float(started_at))

    raw_active = run.get("active_seconds")
    active_seconds = float(raw_active) if isinstance(raw_active, (int, float)) and raw_active > 0 else None

    game_switches = int(run.get("game_switches") or 0)

    pace_basis = active_seconds if (active_seconds is not None and active_seconds >= 60.0) else elapsed_seconds
    checks_per_hour: float | None = None
    if pace_basis is not None and pace_basis >= 60.0 and overall.checked > 0:
        checks_per_hour = overall.checked / (pace_basis / 3600.0)

    rank_title = _pick_rank(overall, goal_key, item_pool, items_trap)

    return EndStats(
        player_name=player_name,
        seed_name=seed_name,
        goal_key=goal_key,
        goal_label=goal_label,
        goal_detail=goal_detail,
        item_pool=item_pool,
        rank_title=rank_title,
        overall=overall,
        oot=oot,
        mm=mm,
        dungeons=dungeons,
        overworld=overworld,
        bosses_defeated=bosses_defeated,
        boss_order=boss_order,
        triforce_collected=triforce_collected,
        triforce_required=triforce_required,
        triforce_local=triforce_local,
        triforce_remote=triforce_remote,
        triforce_aspects=triforce_aspects,
        items_received_total=items_received_total,
        items_delivered=items_delivered,
        items_progression=items_progression,
        items_useful=items_useful,
        items_filler=items_filler,
        items_trap=items_trap,
        items_oot=items_oot,
        items_mm=items_mm,
        items_shared=items_shared,
        top_senders=top_senders,
        top_trickster=top_trickster,
        top_check_types=top_check_types,
        completed_dungeons=completed_dungeons,
        top_scenes=top_scenes,
        elapsed_seconds=elapsed_seconds,
        active_seconds=active_seconds,
        game_switches=game_switches,
        checks_per_hour=checks_per_hour,
    )


def _ascii_bar(bucket: CheckBucket, width: int = 16) -> str:
    if bucket.total <= 0:
        return "[" + "-" * width + "]"
    filled = round(width * bucket.checked / bucket.total)
    filled = max(0, min(width, filled))
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def format_text_report(stats: EndStats) -> str:
    """Format a clean plain-text summary for the client log and clipboard sharing."""
    lines = [
        "=" * 56,
        "  OOTxMM VICTORY — END STATS",
        "=" * 56,
        f"  Player : {stats.player_name}   |   Seed: {stats.seed_name}",
        f"  Goal   : {stats.goal_label}",
        f"  Result : {stats.goal_detail}",
        f"  Rank   : {stats.rank_title}  (Pool: {stats.item_pool.title()})",
        "-" * 56,
        f"  Overall   {_ascii_bar(stats.overall)} {stats.overall.checked}/{stats.overall.total} ({stats.overall.percent:.1f}%)",
        f"  OoT       {_ascii_bar(stats.oot)} {stats.oot.checked}/{stats.oot.total} ({stats.oot.percent:.1f}%)",
        f"  MM        {_ascii_bar(stats.mm)} {stats.mm.checked}/{stats.mm.total} ({stats.mm.percent:.1f}%)",
        f"  Dungeons  {_ascii_bar(stats.dungeons)} {stats.dungeons.checked}/{stats.dungeons.total} ({stats.dungeons.percent:.1f}%)",
        f"  Overworld {_ascii_bar(stats.overworld)} {stats.overworld.checked}/{stats.overworld.total} ({stats.overworld.percent:.1f}%)",
        "-" * 56,
        (
            f"  Items Received: {stats.items_received_total} "
            f"(Prog: {stats.items_progression}, Useful: {stats.items_useful}, "
            f"Filler: {stats.items_filler}, Traps: {stats.items_trap})"
        ),
    ]
    if stats.items_oot or stats.items_mm or stats.items_shared:
        lines.append(
            f"  By Game       : OoT {stats.items_oot} | MM {stats.items_mm} | Shared {stats.items_shared}"
        )
    if stats.top_senders:
        senders_str = ", ".join(
            f"{s.name} ({s.total}, {s.progression} prog)" for s in stats.top_senders[:3]
        )
        lines.append(f"  Top Senders   : {senders_str}")
    if stats.top_trickster:
        lines.append(f"  Top Trickster : {stats.top_trickster.name} ({stats.top_trickster.traps} traps)")
    if stats.top_check_types:
        kinds = ", ".join(f"{label} {b.checked}/{b.total}" for label, b in stats.top_check_types[:4])
        lines.append(f"  Top Checks    : {kinds}")
    if stats.completed_dungeons:
        lines.append(f"  100% Dungeons : {len(stats.completed_dungeons)} ({', '.join(stats.completed_dungeons[:4])}"
                     f"{'...' if len(stats.completed_dungeons) > 4 else ''})")

    telemetry: list[str] = []
    if stats.elapsed_seconds is not None:
        telemetry.append(f"Elapsed: {format_duration(stats.elapsed_seconds)}")
    if stats.active_seconds is not None:
        telemetry.append(f"Active: {format_duration(stats.active_seconds)}")
    if stats.checks_per_hour is not None:
        telemetry.append(f"Pace: {stats.checks_per_hour:.1f} checks/hr")
    if stats.game_switches:
        telemetry.append(f"OoT<->MM Switches: {stats.game_switches}")
    if telemetry:
        lines.append("-" * 56)
        lines.append("  " + "  |  ".join(telemetry))

    lines.append("=" * 56)
    return "\n".join(lines)


def _build_kivy_widget(stats: EndStats, on_back=None):
    """Build the Kivy End Stats screen widget. Imports Kivy lazily."""
    from kivy.core.clipboard import Clipboard
    from kivy.graphics import Color, RoundedRectangle
    from kivy.metrics import dp
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.label import Label
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.widget import Widget

    # Palette: dark slate background with Zelda gold, OoT emerald, MM violet accents.
    BG_CARD = (0.13, 0.14, 0.19, 1)
    BG_HEADER = (0.17, 0.15, 0.09, 1)
    BORDER_GOLD = (0.88, 0.72, 0.25, 1)
    ACCENT_GOLD = (0.95, 0.80, 0.30, 1)
    ACCENT_OOT = (0.25, 0.78, 0.45, 1)
    ACCENT_MM = (0.68, 0.42, 0.92, 1)
    ACCENT_CYAN = (0.30, 0.76, 0.92, 1)
    ACCENT_CORAL = (0.94, 0.44, 0.44, 1)
    TEXT_PRIMARY = (0.95, 0.96, 0.98, 1)
    TEXT_MUTED = (0.72, 0.75, 0.82, 1)
    BAR_TRACK = (0.22, 0.24, 0.30, 1)

    def _add_card_bg(widget: Widget, rgba: tuple[float, float, float, float], radius: float = 8.0) -> None:
        with widget.canvas.before:
            Color(*rgba)
            rect = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[dp(radius)])
        widget.bind(
            pos=lambda inst, val: setattr(rect, "pos", val),
            size=lambda inst, val: setattr(rect, "size", val),
        )

    def _auto_label(
        text: str,
        *,
        font_size: str = "14sp",
        color: tuple[float, float, float, float] = TEXT_PRIMARY,
        bold: bool = False,
        halign: str = "left",
        markup: bool = False,
    ) -> Label:
        lbl = Label(
            text=text,
            font_size=font_size,
            color=color,
            bold=bold,
            halign=halign,
            valign="middle",
            markup=markup,
            size_hint_y=None,
        )
        lbl.bind(
            width=lambda inst, w: setattr(inst, "text_size", (max(1, w), None)),
            texture_size=lambda inst, ts: setattr(inst, "height", max(dp(20), ts[1] + dp(4))),
        )
        return lbl

    def _make_card(title: str | None = None, title_color=ACCENT_GOLD, bg=BG_CARD) -> BoxLayout:
        card = BoxLayout(
            orientation="vertical",
            padding=[dp(14), dp(12), dp(14), dp(12)],
            spacing=dp(6),
            size_hint_y=None,
        )
        card.bind(minimum_height=card.setter("height"))
        _add_card_bg(card, bg)
        if title:
            card.add_widget(_auto_label(title, font_size="15sp", color=title_color, bold=True))
        return card

    def _make_progress_row(label: str, bucket: CheckBucket, bar_color) -> BoxLayout:
        row = BoxLayout(orientation="vertical", spacing=dp(3), size_hint_y=None, height=dp(38))
        top = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(20))
        top.add_widget(_auto_label(label, font_size="13sp", color=TEXT_PRIMARY, bold=True))
        top.add_widget(
            _auto_label(
                f"{bucket.checked} / {bucket.total}  ({bucket.percent:.1f}%)",
                font_size="13sp",
                color=TEXT_MUTED,
                halign="right",
            )
        )
        row.add_widget(top)

        bar = Widget(size_hint_y=None, height=dp(10))
        ratio = (bucket.checked / bucket.total) if bucket.total > 0 else 0.0
        ratio = max(0.0, min(1.0, ratio))
        with bar.canvas:
            Color(*BAR_TRACK)
            track_rect = RoundedRectangle(pos=bar.pos, size=bar.size, radius=[dp(4)])
            Color(*bar_color)
            fill_rect = RoundedRectangle(pos=bar.pos, size=(bar.width * ratio, bar.height), radius=[dp(4)])

        def _update_bar(inst, _val):
            track_rect.pos = inst.pos
            track_rect.size = inst.size
            fill_rect.pos = inst.pos
            fill_rect.size = (inst.width * ratio, inst.height)

        bar.bind(pos=_update_bar, size=_update_bar)
        row.add_widget(bar)
        return row

    scroll = ScrollView(do_scroll_x=False, bar_width=dp(8))
    root = BoxLayout(
        orientation="vertical",
        padding=[dp(16), dp(14), dp(16), dp(20)],
        spacing=dp(12),
        size_hint_y=None,
    )
    root.bind(minimum_height=root.setter("height"))

    # --- Victory Header Card ---
    header = _make_card(bg=BG_HEADER)
    header.add_widget(
        _auto_label("VICTORY — OOTxMM END STATS", font_size="21sp", color=ACCENT_GOLD, bold=True, halign="center")
    )
    header.add_widget(
        _auto_label(
            f"{stats.rank_title}",
            font_size="16sp",
            color=TEXT_PRIMARY,
            bold=True,
            halign="center",
        )
    )
    header.add_widget(
        _auto_label(
            f"Player: {stats.player_name}   •   Goal: {stats.goal_label}   •   Pool: {stats.item_pool.title()}",
            font_size="13sp",
            color=TEXT_MUTED,
            halign="center",
        )
    )
    header.add_widget(
        _auto_label(
            stats.goal_detail,
            font_size="14sp",
            color=BORDER_GOLD,
            bold=True,
            halign="center",
        )
    )
    root.add_widget(header)

    # --- Completion Progress Card ---
    prog_card = _make_card("WORLD COMPLETION", title_color=ACCENT_GOLD)
    prog_card.add_widget(_make_progress_row("Overall Checks", stats.overall, ACCENT_GOLD))
    prog_card.add_widget(_make_progress_row("Ocarina of Time", stats.oot, ACCENT_OOT))
    prog_card.add_widget(_make_progress_row("Majora's Mask", stats.mm, ACCENT_MM))
    prog_card.add_widget(_make_progress_row("Dungeons", stats.dungeons, ACCENT_CYAN))
    prog_card.add_widget(_make_progress_row("Overworld", stats.overworld, (0.45, 0.80, 0.65, 1)))
    root.add_widget(prog_card)

    # --- Two-column Grid for Items & Telemetry ---
    mid_grid = GridLayout(cols=2, spacing=dp(12), size_hint_y=None)
    mid_grid.bind(minimum_height=mid_grid.setter("height"))

    items_card = _make_card("MULTIWORLD ITEMS", title_color=ACCENT_CYAN)
    items_card.add_widget(_auto_label(f"Total Received: {stats.items_received_total}  (Delivered: {stats.items_delivered})", bold=True))
    items_card.add_widget(_auto_label(f"Progression: {stats.items_progression}", color=ACCENT_GOLD))
    items_card.add_widget(_auto_label(f"Useful: {stats.items_useful}", color=ACCENT_CYAN))
    items_card.add_widget(_auto_label(f"Filler: {stats.items_filler}", color=TEXT_MUTED))
    items_card.add_widget(_auto_label(f"Traps: {stats.items_trap}", color=ACCENT_CORAL if stats.items_trap else TEXT_MUTED))
    items_card.add_widget(
        _auto_label(
            f"By Game: OoT {stats.items_oot}  |  MM {stats.items_mm}  |  Shared {stats.items_shared}",
            font_size="12sp",
            color=TEXT_MUTED,
        )
    )
    mid_grid.add_widget(items_card)

    run_card = _make_card("RUN TELEMETRY", title_color=ACCENT_MM)
    run_card.add_widget(_auto_label(f"Elapsed Time: {format_duration(stats.elapsed_seconds)}", bold=True))
    run_card.add_widget(_auto_label(f"Active Play Time: {format_duration(stats.active_seconds)}"))
    pace_text = f"{stats.checks_per_hour:.1f} checks/hr" if stats.checks_per_hour is not None else "--"
    run_card.add_widget(_auto_label(f"Check Pace: {pace_text}"))
    run_card.add_widget(_auto_label(f"OoT <-> MM Switches: {stats.game_switches}"))
    if stats.bosses_defeated:
        run_card.add_widget(_auto_label(f"Bosses Cleared: {' -> '.join(stats.boss_order)}", color=ACCENT_GOLD))
    run_card.add_widget(_auto_label(f"Seed: {stats.seed_name}", font_size="12sp", color=TEXT_MUTED))
    mid_grid.add_widget(run_card)

    root.add_widget(mid_grid)

    # --- Two-column Grid for Top Senders & Check Highlights ---
    low_grid = GridLayout(cols=2, spacing=dp(12), size_hint_y=None)
    low_grid.bind(minimum_height=low_grid.setter("height"))

    senders_card = _make_card("TOP MULTIWORLD SENDERS", title_color=ACCENT_OOT)
    if stats.top_senders:
        for idx, sender in enumerate(stats.top_senders, 1):
            extra = f" ({sender.progression} prog" + (f", {sender.traps} traps)" if sender.traps else ")")
            senders_card.add_widget(
                _auto_label(f"{idx}. {sender.name} — {sender.total} items{extra}", font_size="13sp")
            )
    else:
        senders_card.add_widget(_auto_label("Solo / local run — no remote senders.", font_size="13sp", color=TEXT_MUTED))
    if stats.top_trickster:
        senders_card.add_widget(
            _auto_label(
                f"Top Trickster: {stats.top_trickster.name} ({stats.top_trickster.traps} traps)",
                font_size="13sp",
                color=ACCENT_CORAL,
                bold=True,
            )
        )
    low_grid.add_widget(senders_card)

    checks_card = _make_card("CHECK HIGHLIGHTS", title_color=ACCENT_GOLD)
    if stats.top_check_types:
        for label, bucket in stats.top_check_types:
            checks_card.add_widget(
                _auto_label(f"{label}: {bucket.checked}/{bucket.total} ({bucket.percent:.0f}%)", font_size="13sp")
            )
    else:
        checks_card.add_widget(_auto_label("No check breakdown recorded.", font_size="13sp", color=TEXT_MUTED))
    if stats.completed_dungeons:
        shown = ", ".join(stats.completed_dungeons[:5])
        suffix = f" (+{len(stats.completed_dungeons) - 5} more)" if len(stats.completed_dungeons) > 5 else ""
        checks_card.add_widget(
            _auto_label(f"100% Dungeons ({len(stats.completed_dungeons)}): {shown}{suffix}", font_size="12sp", color=ACCENT_OOT)
        )
    low_grid.add_widget(checks_card)

    root.add_widget(low_grid)

    # --- Action Buttons ---
    actions = BoxLayout(orientation="horizontal", spacing=dp(12), size_hint_y=None, height=dp(42))
    report_text = format_text_report(stats)

    copy_btn = Button(
        text="Copy Stats to Clipboard",
        size_hint_x=0.6,
        background_color=(0.24, 0.52, 0.34, 1),
        color=TEXT_PRIMARY,
        bold=True,
    )

    def _copy(_inst):
        try:
            Clipboard.copy(report_text)
            copy_btn.text = "Copied!"
        except Exception:
            copy_btn.text = "Clipboard Unavailable"

    copy_btn.bind(on_release=_copy)
    actions.add_widget(copy_btn)

    if on_back is not None:
        back_btn = Button(
            text="Back to Log",
            size_hint_x=0.4,
            background_color=(0.25, 0.27, 0.35, 1),
            color=TEXT_PRIMARY,
        )
        back_btn.bind(on_release=lambda _inst: on_back())
        actions.add_widget(back_btn)

    root.add_widget(actions)
    scroll.add_widget(root)
    return scroll


def show_end_stats_tab(ctx: "BizHawkClientContext", stats: EndStats, existing_tab=None):
    """Add (or replace) the 'End Stats' tab in Archipelago's Kivy UI and switch to it.

    Returns the tab reference (or None if no GUI is active). Safe to call from async tasks.
    """
    ui = getattr(ctx, "ui", None)
    if ui is None or not hasattr(ui, "add_client_tab"):
        return None

    holder = {"tab": existing_tab}

    def _open(_dt=0):
        try:
            if holder["tab"] is not None and hasattr(ui, "remove_client_tab"):
                try:
                    ui.remove_client_tab(holder["tab"])
                except Exception:
                    pass
                holder["tab"] = None

            def _back():
                try:
                    if hasattr(ui, "tabs") and ui.tabs.children:
                        # Switch back to the first (leftmost) tab, which is the main log tab.
                        ui.tabs.children[-1].on_release()
                except Exception:
                    pass

            widget = _build_kivy_widget(stats, on_back=_back)
            tab = ui.add_client_tab(END_STATS_TAB_TITLE, widget)
            holder["tab"] = tab
            if hasattr(tab, "on_release"):
                tab.on_release()
        except Exception:
            logger.debug("Could not open End Stats UI tab", exc_info=True)

    try:
        from kivy.clock import Clock
        Clock.schedule_once(_open, 0)
    except Exception:
        # Fallback if running with a mock UI in unit tests without Kivy installed.
        _open(0)
    return holder
