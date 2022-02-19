# -*- coding: utf-8 -*-

# Thirdparty:
import ormar
from casbin import Model, persist


class Filter:  # pylint: disable=too-few-public-methods
    """
    Filter class for ormar-based Casbin adapter.
    """

    ptype: list[str] = []
    v0: list[str] = []
    v1: list[str] = []
    v2: list[str] = []
    v3: list[str] = []
    v4: list[str] = []
    v5: list[str] = []


class DatabasesAdapter(persist.Adapter):
    """
    Adapter class for ormar-based Casbin adapter.
    """

    cols = ["ptype"] + [f"v{i}" for i in range(6)]

    def __init__(self, model: ormar.Model, filtered: bool = False) -> None:
        self.model: ormar.Model = model
        self.filtered: bool = filtered

    async def load_policy(self, model: Model) -> None:
        """loads all policy rules from the storage."""

        rows = await self.model.objects.all()
        for row in rows:
            # convert row.dict() to csv format and removing the first column (id)
            line = [
                v for k, v in row.dict().items() if k in self.cols and v is not None
            ]
            persist.load_policy_line(", ".join(line), model)

    async def save_policy(self, model: Model) -> bool:
        """saves all policy rules to the storage."""

        rules = await self.model.objects.all()
        for rule in rules:
            await rule.delete()

        values: list[dict[str, str]] = []
        for sec in ["p", "g"]:

            if sec not in model.model.keys():  # pragma: no cover
                continue

            for p_type, assertion in model.model[sec].items():
                for rule in assertion.policy:
                    row = self._policy_to_dict(p_type, rule)
                    values.append(row)

        await self.model.objects.bulk_create([self.model(**value) for value in values])
        return True

    # pylint: disable=unused-argument
    async def add_policy(self, sec: str, p_type: str, rule: list[str]) -> None:
        """adds a policy rule to the storage."""

        row = self._policy_to_dict(p_type, rule)
        await self.model(**row).save()

    # pylint: disable=unused-argument
    async def remove_policy(self, sec: str, p_type: str, rule: list[str]) -> bool:
        """removes a policy rule from the storage."""

        query = self.model.objects.filter(ptype=p_type)
        for i, value in enumerate(rule):
            query = query.filter(**{f"v{i}": value})

        result = await query.get_or_none()

        return result is not None

    # pylint: disable=unused-argument
    async def remove_filtered_policy(
        self, sec: str, ptype: str, field_index: int, *field_values: tuple[str]
    ) -> bool:
        """removes policy rules that match the filter from the storage.
        This is part of the Auto-Save feature.
        """

        query = self.model.objects.filter(ptype=ptype)
        if not 0 <= field_index <= 5:  # pragma: no cover
            return False
        if not 1 <= field_index + len(field_values) <= 6:  # pragma: no cover
            return False
        for _, value in enumerate(field_values):
            if len(value) > 0:
                query = query.filter(**{f"v{field_index+1}": value})
        result = await query.get_or_none()
        return result is not None

    async def load_filtered_policy(self, model: Model, filter_: Filter) -> None:
        """loads policy rules that match the filter from the storage."""

        query = self.model.objects.order_by("id")
        for att, value in filter_.__dict__.items():
            if len(value) > 0:
                query = query.filter(**{f"{att}__in": value})
        rows = await query.all()
        for row in rows:
            # convert row.dict() to csv format and removing the first column (id)
            line = [
                v for k, v in row.dict().items() if k in self.cols and v is not None
            ]
            persist.load_policy_line(", ".join(line), model)

    def is_filtered(self) -> bool:
        """returns whether the adapter is filtered or not."""

        return self.filtered

    @staticmethod
    def _policy_to_dict(p_type: str, rule: list[str]) -> dict[str, str]:
        """converts a policy rule to a dictionary."""

        row: dict[str, str] = {"ptype": p_type}
        for i, value in enumerate(rule):
            row.update({f"v{i}": value})
        return row
