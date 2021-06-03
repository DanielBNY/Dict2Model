SOURCE_NAMING_EXCEPTION_MESSAGE = """
Each variable is required to have a source. 
The source naming is the normal variable name plus _SOURCE

An example for a correct class:

class ExampleObj:
    number: int
    question: bool

    NUMBER_SOURCE = "data-number"
    QUESTION_SOURCE = "data-question"


If the variable NUMBER_SOURCE would change to NUMBER_
"""


def is_valid_variable_names(annotations_names, global_dict):
    for name in annotations_names:
        if f"{name.upper()}_SOURCE" not in global_dict:
            raise Exception(SOURCE_NAMING_EXCEPTION_MESSAGE)
    return True
