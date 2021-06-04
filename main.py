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

SOURCE_FORMAT_EXPLANATION = f"""
The sources value format and type:

The sources variable define the path inside a dictionary to get the desired value.
For example 'NUMBER_SOURCE = data{SOURCE_SEPARATION_CHAR}info{SOURCE_SEPARATION_CHAR}extra{SOURCE_SEPARATION_CHAR}number' is equivalent to: 
value = input_dict["data"]["info"]["extra"]["number"]

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
                    type_exception(expected_type=self.class_annotations[variable_name], variable_name=variable_name,
                                   variable_value=variable_input)

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
        self._validate_source_type_str()

    def _validate_source_existence(self):
        for name in self.class_annotations:
            if f"{name.upper()}_SOURCE" not in self.class_attr:
                raise Exception(SOURCE_NAMING_EXCEPTION_MESSAGE)
        return True

    def _validate_source_type_str(self):
        for attr_key in self.class_attr:
            if "_SOURCE" in attr_key:
                attr_value = self.class_attr.get(attr_key)
                if type(attr_value) is not str:
                    type_exception(expected_type=str, variable_name=attr_key, variable_value=attr_value,
                                   requirement_explanation=SOURCE_FORMAT_EXPLANATION)


def type_exception(expected_type: type, variable_name: str, variable_value, requirement_explanation=""):
    raise TypeError(f"\n\nInput for variable '{variable_name}' is '{variable_value}' in type {type(variable_value)}, "
                    f"expected type {expected_type}\n"
                    f"{requirement_explanation}\n")
