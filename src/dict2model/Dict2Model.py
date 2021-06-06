#
# MIT License
#
# Copyright (c) 2021 DanielBNY
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .Dict2ModelConsts import *


class Dict2Model:

    def __init__(self, input_class: type, input_dict: dict):
        self._init_input_params(input_class, input_dict)
        self._validate_input()
        self._init_extra_attributes()
        self._validate_usages_in_class()

    def _init_input_params(self, input_class, input_dict):
        self._input_class = input_class
        self._input_dict = input_dict

    def _init_extra_attributes(self):
        self._class_attr = self._input_class.__dict__
        self._class_annotations = self._class_attr.get('__annotations__')
        self._disable_type_exception = bool(self._class_attr.get(DISABLE_TYPE_EXCEPTIONS))
        self._disable_path_exception = bool(self._class_attr.get(DISABLE_PATH_EXCEPTIONS))
        self.log = ""

    def run(self):
        self._insert_values_to_class()
        return self._input_class

    def _insert_values_to_class(self):
        for variable_name in self._class_annotations:
            annotation_type = self._class_annotations.get(variable_name)
            variable_input = self._get_input_from_source(variable_name)
            if type(variable_input) is annotation_type:
                setattr(self._input_class, variable_name, variable_input)
            else:
                exception_message = get_type_exception_message(expected_type=annotation_type,
                                                               variable_value=variable_input,
                                                               variable_name=variable_name)
                self.type_exception_or_log(disable_exception=self._disable_type_exception,
                                           exception_message=exception_message)
                if self._disable_type_exception:
                    setattr(self._input_class, variable_name, None)

    def _get_input_from_source(self, variable_name):
        source_dict_path_str: str = self._class_attr.get(f"{variable_name.upper()}{SOURCE_SUFFIX}")
        source_dict_path_list: list = source_dict_path_str.split(SOURCE_SEPARATION_CHAR)
        data = self._input_dict
        for key in source_dict_path_list:
            if data:
                data = data.get(key)
                if data is None:
                    exception_message = f"\nThe path {str(source_dict_path_list)} in dict {self._input_dict} don't exist\n" \
                                        f"{SOURCE_FORMAT_EXPLANATION}"
                    self.normal_exception_or_log(disable_exception=self._disable_path_exception,
                                                 exception_message=exception_message)
        return data

    def type_exception_or_log(self, disable_exception: bool, exception_message: str):
        try:
            raise TypeError(exception_message)
        except TypeError as ex:
            if not disable_exception:
                raise ex
            self.log += exception_message

    def normal_exception_or_log(self, disable_exception: bool, exception_message: str):
        try:
            raise Exception(exception_message)
        except Exception as ex:
            if not disable_exception:
                raise ex
            self.log += exception_message

    # Usages Validations
    def _validate_input(self):
        self._validate_dict_input()
        self._validate_class_input_type()

    def _validate_usages_in_class(self):
        self._validate_annotation_existence()
        self._validate_sources_for_annotations()
        self._validate_source_type_str()
        self._validate_annotations_for_sources()

    def _validate_annotations_for_sources(self):
        for attr_key in self._class_attr:
            if SOURCE_SUFFIX in attr_key:
                source_variable = attr_key
                required_annotation = source_variable.replace(SOURCE_SUFFIX, '').lower()
                if required_annotation not in self._class_annotations:
                    raise Exception(f"No annotation variable '{required_annotation}'\n"
                                    f"{ANNOTATION_FOR_SOURCES}")

    def _validate_class_input_type(self):
        if type(self._input_class) is not type:
            type_exception_message = get_type_exception_message(expected_type=type, variable_name="input_class",
                                                                variable_value=self._input_class,
                                                                requirement_explanation=CLASS_REQUIREMENT_EXPLANATION)
            raise TypeError(type_exception_message)

    def _validate_annotation_existence(self):
        if not self._class_annotations:
            raise Exception(f"\nNo annotation variables in {self._input_class}.\n"
                            f"{ANNOTATION_VARIABLE_EXPLANATION}")

    def _validate_dict_input(self):
        if type(self._input_dict) is not dict:
            type_exception_message = get_type_exception_message(expected_type=dict, variable_name='input_dict',
                                                                variable_value=self._input_dict)
            raise TypeError(type_exception_message)

    def _validate_sources_for_annotations(self):
        for name in self._class_annotations:
            if f"{name.upper()}{SOURCE_SUFFIX}" not in self._class_attr:
                raise Exception(f"\nNo source variable {name.upper() + SOURCE_SUFFIX}\n"
                                f"{SOURCE_NAMING_EXCEPTION_MESSAGE}")

    def _validate_source_type_str(self):
        for attr_key in self._class_attr:
            if SOURCE_SUFFIX in attr_key:
                attr_value = self._class_attr.get(attr_key)
                if type(attr_value) is not str:
                    exception_message = get_type_exception_message(expected_type=str, variable_name=attr_key,
                                                                   variable_value=attr_value,
                                                                   requirement_explanation=SOURCE_FORMAT_EXPLANATION)
                    raise TypeError(exception_message)


def get_type_exception_message(expected_type: type, variable_name: str, variable_value, requirement_explanation=""):
    return f"Input for variable '{variable_name}' is '{variable_value}' in type {type(variable_value)}, " \
           f"expected type {expected_type}\n" \
           f"{requirement_explanation}"
