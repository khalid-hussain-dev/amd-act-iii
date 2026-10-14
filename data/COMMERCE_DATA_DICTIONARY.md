# LotLens Synthetic Commerce Snapshot — Data Dictionary

The built-in Commerce scenario is fictional data used to demonstrate how a quality alert can inform stock and order review. It is not a real inventory record and does not predict future demand.

## Inventory snapshot CSV

One row maps a product SKU to a production lot.

| Column | Type | Meaning |
| --- | --- | --- |
| `sku` | Text | Product identifier. |
| `product_name` | Text | Human-readable product name. |
| `batch_id` | Text | Lot/batch identifier. This must match `batch_id` in production readings to identify affected stock. |
| `on_hand_units` | Whole number | Units physically listed as on hand for the lot. |
| `reserved_units` | Whole number | Units already committed to orders; cannot exceed on-hand units. |

## Open-orders CSV

One row per SKU aggregates units on open orders that are not yet reserved to a lot.

| Column | Type | Meaning |
| --- | --- | --- |
| `sku` | Text | Product identifier, matching the inventory snapshot. |
| `unallocated_open_order_units` | Whole number | Open-order units that still need stock allocation. |

## Demonstration rule

For each SKU mapped to the quality-alert batch, LotLens calculates:

```text
clean available = sum(on_hand_units - reserved_units) across other lots for that SKU
reallocation need = reserved units in the alerted lot + unallocated open-order units
reallocation capacity = min(clean available, reallocation need)
uncovered units = max(0, reallocation need - clean available)
```

This produces a prompt for a quality or fulfillment lead to review a temporary hold and possible allocation from unaffected lots. LotLens does not place a hold, modify orders, issue a replenishment request, infer a root cause, or forecast sales. An uploaded production CSV must be accompanied by both an inventory snapshot and an open-orders CSV to show its Commerce impact. The user-reported Track 1 checks do not verify this newly added Commerce workflow.
