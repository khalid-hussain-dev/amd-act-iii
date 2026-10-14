"""Deterministic inventory impact and allocation guidance for Commerce."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd


INVENTORY_COLUMNS = {
    "sku",
    "product_name",
    "batch_id",
    "on_hand_units",
    "reserved_units",
}
ORDER_COLUMNS = {"sku", "unallocated_open_order_units"}
COUNT_COLUMNS = ("on_hand_units", "reserved_units")


@dataclass(frozen=True)
class CommerceInput:
    valid: bool
    errors: list[str]
    inventory: pd.DataFrame | None = None
    orders: pd.DataFrame | None = None


def sample_inventory() -> pd.DataFrame:
    """Return a fictional lot-to-SKU inventory snapshot for the seeded demo."""
    return pd.DataFrame(
        [
            {"sku": "ACT-HSG-04", "product_name": "Precision actuator housing", "batch_id": "LOT-8042-A", "on_hand_units": 320, "reserved_units": 90},
            {"sku": "ACT-HSG-04", "product_name": "Precision actuator housing", "batch_id": "LOT-8042-B", "on_hand_units": 180, "reserved_units": 65},
        ]
    )


def sample_orders() -> pd.DataFrame:
    """Return the unallocated order demand for the fictional demo SKU."""
    return pd.DataFrame([{"sku": "ACT-HSG-04", "unallocated_open_order_units": 120}])


def validate_commerce_inputs(inventory: pd.DataFrame, orders: pd.DataFrame) -> CommerceInput:
    """Validate inventory and unallocated order snapshots without mutating them."""
    missing_inventory = sorted(INVENTORY_COLUMNS - set(inventory.columns))
    missing_orders = sorted(ORDER_COLUMNS - set(orders.columns))
    if missing_inventory or missing_orders:
        errors = []
        if missing_inventory:
            errors.append(f"Inventory CSV is missing: {', '.join(missing_inventory)}.")
        if missing_orders:
            errors.append(f"Open-orders CSV is missing: {', '.join(missing_orders)}.")
        return CommerceInput(False, errors)
    if inventory.empty:
        return CommerceInput(False, ["Inventory CSV must contain at least one lot row."])
    if orders.empty:
        return CommerceInput(False, ["Open-orders CSV must contain at least one SKU row."])

    stock = inventory.copy()
    demand = orders.copy()
    for column in (*COUNT_COLUMNS, "unallocated_open_order_units"):
        target = stock if column in COUNT_COLUMNS else demand
        target[column] = pd.to_numeric(target[column], errors="coerce")
        if target[column].isna().any() or not np.isfinite(target[column].to_numpy(dtype=float)).all():
            return CommerceInput(False, [f"`{column}` must contain finite numeric counts."])
        if (target[column] < 0).any() or not np.equal(target[column], np.floor(target[column])).all():
            return CommerceInput(False, [f"`{column}` must contain non-negative whole-number counts."])

    for column in ("sku", "product_name", "batch_id"):
        stock[column] = stock[column].fillna("").astype(str).str.strip()
        if (stock[column] == "").any():
            return CommerceInput(False, [f"`{column}` must be present for every inventory row."])
    demand["sku"] = demand["sku"].fillna("").astype(str).str.strip()
    if (demand["sku"] == "").any():
        return CommerceInput(False, ["`sku` must be present for every open-orders row."])
    if (stock["reserved_units"] > stock["on_hand_units"]).any():
        return CommerceInput(False, ["`reserved_units` cannot exceed `on_hand_units`."])
    if stock.duplicated(["sku", "batch_id"]).any():
        return CommerceInput(False, ["Inventory must have one row per SKU and batch."])
    if demand["sku"].duplicated().any():
        return CommerceInput(False, ["Open orders must have one aggregated row per SKU."])

    return CommerceInput(True, [], stock, demand)


def calculate_inventory_impact(
    affected_batch: str,
    inventory: pd.DataFrame,
    orders: pd.DataFrame,
) -> dict[str, Any]:
    """Map a quality-alert batch to exposed stock and a rule-based allocation."""
    affected = inventory.loc[inventory["batch_id"] == affected_batch]
    if affected.empty:
        return {"status": "unmapped", "affected_batch": affected_batch, "products": []}

    products: list[dict[str, Any]] = []
    for sku in affected["sku"].drop_duplicates().tolist():
        sku_stock = inventory.loc[inventory["sku"] == sku].copy()
        impacted = sku_stock.loc[sku_stock["batch_id"] == affected_batch]
        clean = sku_stock.loc[sku_stock["batch_id"] != affected_batch]
        order_rows = orders.loc[orders["sku"] == sku, "unallocated_open_order_units"]
        open_orders = int(order_rows.iloc[0]) if not order_rows.empty else 0
        affected_on_hand = int(impacted["on_hand_units"].sum())
        affected_reserved = int(impacted["reserved_units"].sum())
        clean_available = int((clean["on_hand_units"] - clean["reserved_units"]).sum())
        reallocation_need = affected_reserved + open_orders
        reallocated = min(clean_available, reallocation_need)
        shortfall = max(0, reallocation_need - clean_available)
        products.append(
            {
                "sku": sku,
                "product_name": str(impacted["product_name"].iloc[0]),
                "affected_on_hand": affected_on_hand,
                "affected_reserved": affected_reserved,
                "clean_available": clean_available,
                "unallocated_open_orders": open_orders,
                "reallocation_need": reallocation_need,
                "reallocated": reallocated,
                "shortfall": shortfall,
                "clean_remaining": clean_available - reallocated,
            }
        )
    return {"status": "mapped", "affected_batch": affected_batch, "products": products}
