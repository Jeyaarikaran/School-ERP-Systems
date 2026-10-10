"""Widget Framework — Dynamic, isolated dashboard widgets."""

from typing import Any, Callable, Dict, Protocol
from uuid import UUID

from pydantic import BaseModel


class WidgetContext(BaseModel):
    """Context passed to every widget loader."""
    tenant_id: UUID
    user_id: UUID
    role: str
    date_range: tuple[str, str] | None = None
    filters: dict[str, Any] = {}


class WidgetResult(BaseModel):
    """Standardized widget output."""
    status: str  # ok, empty, error, forbidden
    data: dict[str, Any] | None = None
    as_of: str | None = None
    error_code: str | None = None


class WidgetLoader(Protocol):
    async def load(self, context: WidgetContext) -> WidgetResult:
        ...


class WidgetRegistry:
    """Registry of all available dashboard widgets."""

    def __init__(self) -> None:
        self._widgets: Dict[str, WidgetLoader] = {}
        self._role_layouts: Dict[str, list[dict[str, Any]]] = {}

    def register(self, key: str, loader: WidgetLoader) -> None:
        self._widgets[key] = loader

    def register_role_layout(self, role: str, layout: list[dict[str, Any]]) -> None:
        self._role_layouts[role] = layout

    def get_layout(self, role: str) -> list[dict[str, Any]]:
        return self._role_layouts.get(role, [])

    async def load_widget(self, key: str, context: WidgetContext) -> WidgetResult:
        loader = self._widgets.get(key)
        if not loader:
            return WidgetResult(status="error", error_code="WIDGET_NOT_FOUND")
            
        try:
            return await loader.load(context)
        except Exception:
            # Fallback for widget isolation: one bad widget shouldn't break the dashboard
            return WidgetResult(status="error", error_code="WIDGET_LOAD_FAILED")


widget_registry = WidgetRegistry()
