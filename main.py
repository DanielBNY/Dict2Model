SOURCE_SEPARATION_CHAR = "-"

SOURCE_NAMING_EXCEPTION_MESSAGE = f"""
Each variable is required to have a source. 
The source naming is the normal variable name plus _SOURCE

An example for a correct class:

class ExampleObj:
    number: int
    question: bool

    NUMBER_SOURCE = "data{SOURCE_SEPARATION_CHAR}number"
    QUESTION_SOURCE = "data{SOURCE_SEPARATION_CHAR}question"


If the variable NUMBER_SOURCE would change to NUMBER_
"""


class SpecialDictModel:

    def __init__(self, input_class, input_data):
        self.input_class = input_class
        self.class_attr = self.input_class.__dict__
        self.class_annotations = self.class_attr.get('__annotations__')
        self.input_data = input_data

    def run(self):
        self._validate_usages_in_class()
        self._insert_values_to_class()
        return self.input_class

    def _insert_values_to_class(self):
        for variable_name in self.class_annotations:
            variable_input = self._get_input_from_source(variable_name)
            if type(variable_input) is self.class_annotations[variable_name]:
                setattr(self.input_class, variable_name, variable_input)
            else:
                if self.class_attr.get("DISABLE_TYPE_EXCEPTIONS"):
                    setattr(self.input_class, variable_name, None)
                else:
                    raise TypeError(
                        f"Input for variable '{variable_name}' is {variable_input} in type {type(variable_input)}, "
                        f"expected type {self.class_annotations[variable_name]}")

    def _get_input_from_source(self, variable_name):
        source = self.class_attr.get(f"{variable_name.upper()}_SOURCE")
        split_source = source.split(SOURCE_SEPARATION_CHAR)
        data = self.input_data
        for part in split_source:
            if data:
                data = data.get(part)
        return data

    # Usages Validations

    def _validate_usages_in_class(self):
        self._validate_source_existence()

    def _validate_source_existence(self):
        for name in self.class_annotations:
            if f"{name.upper()}_SOURCE" not in self.class_attr:
                raise Exception(SOURCE_NAMING_EXCEPTION_MESSAGE)
        return True
