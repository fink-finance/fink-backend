"""ORM models for the application domain."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Transaction(Base):
    """Financial transaction record.

    Attributes:
        id: Surrogate primary key.
        amount: Transaction amount in the default currency.
        description: Optional short free-text description.
        created_at: Row creation timestamp (server clock).
        updated_at: Row last update timestamp (server clock).
    """

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        """Return a concise debug representation."""
        return f"<Transaction id={self.id} amount={self.amount}>"
