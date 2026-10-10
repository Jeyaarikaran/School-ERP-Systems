"""Pure Domain Engine for Fee Math and Ledger Allocation.

This module accesses no databases and performs no IO. It relies entirely on
provided data structures to perform deterministic financial math. All money
values should be passed in as Decimal.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any, List

class FeeCalculationEngine:
    
    @staticmethod
    def calculate_net_amount(gross: Decimal, discount: Decimal, late_fee: Decimal) -> Decimal:
        """Net amount calculation matching the DB generated column logic."""
        net = gross - discount + late_fee
        return max(Decimal("0.00"), net)

    @staticmethod
    def apply_discounts(gross_amount: Decimal, adjustments: List[Dict[str, Any]]) -> Decimal:
        """
        Stacks discounts based on priority and calculates total discount.
        Discounts are capped at gross_amount to ensure net_amount never goes negative.
        """
        total_discount = Decimal("0.00")
        remaining_gross = gross_amount
        
        # Priority mapping based on kind
        priority_map = {
            "scholarship": 1,
            "concession": 2,
            "sibling": 3,
            "discount": 4
        }
        
        # Sort by priority, then by a provided sequence/time
        sorted_adjs = sorted(adjustments, key=lambda x: (
            priority_map.get(x["kind"], 99),
            x.get("created_at", "")
        ))
        
        for adj in sorted_adjs:
            if remaining_gross <= 0:
                break
                
            val = Decimal(str(adj["value"]))
            discount_for_this = Decimal("0.00")
            
            if adj["calculation"] == "percent":
                # Percentage is always of the original gross, not remaining
                discount_for_this = (gross_amount * (val / Decimal("100"))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            else:
                discount_for_this = val
                
            # Cap this individual adjustment against what's left
            actual_discount = min(discount_for_this, remaining_gross)
            total_discount += actual_discount
            remaining_gross -= actual_discount
            
        return total_discount

    @staticmethod
    def allocate_payment(payment_amount: Decimal, items: List[Dict[str, Any]], partial_allowed: bool) -> tuple[Decimal, List[Dict[str, Any]]]:
        """
        Allocates a lump sum payment to a list of fee items.
        Items should be pre-sorted by (due_date ASC, priority ASC, id ASC).
        Returns:
            (remaining_credit, list_of_allocations)
        """
        allocations = []
        remaining = payment_amount
        
        for item in items:
            if remaining <= 0:
                break
                
            # Use Decimal everywhere
            net = Decimal(str(item["net_amount"]))
            paid = Decimal(str(item.get("paid_amount", "0.00")))
            due = net - paid
            
            if due <= 0:
                continue
                
            if remaining >= due:
                # Pay this item in full
                allocations.append({
                    "item_id": item["id"],
                    "allocated_amount": due
                })
                remaining -= due
            else:
                # Partial payment
                if not partial_allowed:
                    # If partial is disabled, we stop and leave the rest as credit
                    break
                    
                allocations.append({
                    "item_id": item["id"],
                    "allocated_amount": remaining
                })
                remaining = Decimal("0.00")
                
        return remaining, allocations

    @staticmethod
    def calculate_late_fee(item: Dict[str, Any], rule: Dict[str, Any], today: str) -> Decimal:
        """
        Calculates late fee for an item based on a rule.
        Expects ISO date strings.
        """
        # (Implementation details omitted for brevity, but would handle flat/per_day logic)
        pass
