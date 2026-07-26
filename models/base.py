from __future__ import annotations

from typing import Any


class BaseModel:
    """
    Base response model.
    """

    def __init__(self, data: dict[str, Any]):
        self.data = data

    def to_dict(self) -> dict[str, Any]:
        return dict(self.data)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def __iter__(self):
        return iter(self.data)

    def items(self):
        return self.data.items()

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def update(self, other: "BaseModel"):
        if type(self) is not type(other):
            raise TypeError(
                f"Cannot update {type(self).__name__} "
                f"with {type(other).__name__}"
            )

        self.data = other.data
        return self

    def __len__(self) -> int:
        return len(self.data)

    def __bool__(self) -> bool:
        return bool(self.data)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.data!r})>"

    def __str__(self) -> str:
        return str(self.data)