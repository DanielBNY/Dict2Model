SOURCE_SEPARATION_CHAR = "-"
SOURCE_SUFFIX = "_SOURCE"
DISABLE_TYPE_EXCEPTIONS = "DISABLE_TYPE_EXCEPTIONS"
DISABLE_PATH_EXCEPTIONS = "DISABLE_PATH_EXCEPTIONS"

SOURCE_NAMING_EXCEPTION_MESSAGE = f"""
Each variable is required to have a source. 
The source naming is the normal variable name in upper case plus {SOURCE_SUFFIX}

For example:

class ExampleObj:
    number: int
    question: bool

    NUMBER{SOURCE_SUFFIX} = "data{SOURCE_SEPARATION_CHAR}number"              <----------- Sources
    QUESTION{SOURCE_SUFFIX} = "data{SOURCE_SEPARATION_CHAR}question"       <-----------


If the variable NUMBER{SOURCE_SUFFIX} would change to NUMBER_
"""

SOURCE_FORMAT_EXPLANATION = f"""
The sources value format and type:

The sources variable define the path inside a dictionary to get the desired value.
For example: \
NUMBER{SOURCE_SUFFIX} = 'data{SOURCE_SEPARATION_CHAR}info{SOURCE_SEPARATION_CHAR}extra{SOURCE_SEPARATION_CHAR}number' \
is equivalent to:\nvalue = input_dict["data"]["info"]["extra"]["number"]

to disable exception for none existing path in dictionary add:
{DISABLE_PATH_EXCEPTIONS} = True
If such configuration is added the class attribute value for the non existing value in the dictionary will be 'None'.
"""

ANNOTATION_VARIABLE_EXPLANATION = f"""
Attribute with the required type in an annotation format - (variable: type)
Example inside a class:

class ExampleObj:
    number: int         <-------- annotation
    question: bool   <------  

    NUMBER{SOURCE_SUFFIX} = "data{SOURCE_SEPARATION_CHAR}number"
    QUESTION{SOURCE_SUFFIX} = "data{SOURCE_SEPARATION_CHAR}question"
"""


class DictionaryModelFactory:

    def __init__(self, input_class: type, input_dict: dict):
        self.input_class = input_class
        self.class_attr = self.input_class.__dict__
        self.class_annotations = self.class_attr.get('__annotations__')
        self.input_dict = input_dict
        self.disable_type_exception = bool(self.class_attr.get(DISABLE_TYPE_EXCEPTIONS))
        self.disable_path_exception = bool(self.class_attr.get(DISABLE_PATH_EXCEPTIONS))

    def run(self):
        self._validate_usages_in_class()
        self._insert_values_to_class()
        return self.input_class

    def _insert_values_to_class(self):
        for variable_name in self.class_annotations:
            annotation_type = self.class_annotations.get(variable_name)
            variable_input = self._get_input_from_source(variable_name)
            if type(variable_input) is annotation_type:
                setattr(self.input_class, variable_name, variable_input)
            else:
                if self.disable_type_exception:
                    setattr(self.input_class, variable_name, None)
                else:
                    type_exception(expected_type=annotation_type, variable_name=variable_name,
                                   variable_value=variable_input)

    def _get_input_from_source(self, variable_name):
        source = self.class_attr.get(f"{variable_name.upper()}{SOURCE_SUFFIX}")
        split_source = source.split(SOURCE_SEPARATION_CHAR)
        data = self.input_dict
        for part in split_source:
            if data:
                data = data.get(part)
                if (data is None) and (not self.disable_path_exception):
                    raise Exception(f"\nThe path {str(split_source)} in dict {self.input_dict} don't exist\n"
                                    f"{SOURCE_FORMAT_EXPLANATION}")
        return data

    # Usages Validations

    def _validate_usages_in_class(self):
        self._validate_annotation_existence()
        self._validate_dict_input()
        self._validate_source_existence()
        self._validate_source_type_str()

    def _validate_annotation_existence(self):
        if not self.class_annotations:
            raise Exception(f"\nNo annotation variables in {self.input_class}.\n"
                            f"{ANNOTATION_VARIABLE_EXPLANATION}")

    def _validate_dict_input(self):
        if type(self.input_dict) is not dict:
            raise Exception(f"\nThe given input is not in type <class 'dict'> but in type '{type(self.input_dict)}'")

    def _validate_source_existence(self):
        for name in self.class_annotations:
            if f"{name.upper()}{SOURCE_SUFFIX}" not in self.class_attr:
                raise Exception(SOURCE_NAMING_EXCEPTION_MESSAGE)

    def _validate_source_type_str(self):
        for attr_key in self.class_attr:
            if SOURCE_SUFFIX in attr_key:
                attr_value = self.class_attr.get(attr_key)
                if type(attr_value) is not str:
                    type_exception(expected_type=str, variable_name=attr_key, variable_value=attr_value,
                                   requirement_explanation=SOURCE_FORMAT_EXPLANATION)


def type_exception(expected_type: type, variable_name: str, variable_value, requirement_explanation=""):
    raise TypeError(f"\n\nInput for variable '{variable_name}' is '{variable_value}' in type {type(variable_value)}, "
                    f"expected type {expected_type}\n"
                    f"{requirement_explanation}\n")
