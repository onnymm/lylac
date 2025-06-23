from ...._module_types import (
    CriteriaStructure,
    AutomationMethod,
    AutomationTemplate,
    Transaction,
)

class BaseAutomations():

    def register_automation(
        self,
        model_name: str,
        transaction: Transaction,
        callback: AutomationTemplate,
        fields: list[str] = ['id',],
        criteria: CriteriaStructure = [],
        method: AutomationMethod = 'record'
    ) -> None:
        ...

    def register_model(
        self,
        table: str
    ) -> None:
        ...
