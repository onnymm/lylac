MODEL_TABLE_TEMPLATE = (
"""
class {model_name}(self._base, self._model_template):
    __tablename__ = '{model_name}'

data['model'] = {model_name}
"""
)

