SOURCE_SEPARATION_CHAR = "-"
SOURCE_SUFFIX = "_SOURCE"
DISABLE_TYPE_EXCEPTIONS = "DISABLE_TYPE_EXCEPTIONS"
DISABLE_PATH_EXCEPTIONS = "DISABLE_PATH_EXCEPTIONS"

SOURCE_NAMING_EXCEPTION_MESSAGE = f"""
Each variable is required to have a source. 
The source naming is the normal annotation variable name in upper case plus {SOURCE_SUFFIX}.

For example:

class ExampleObj:
    number: int
    question: bool

    NUMBER{SOURCE_SUFFIX} = "data{SOURCE_SEPARATION_CHAR}number"              <----------- Sources
    QUESTION{SOURCE_SUFFIX} = "data{SOURCE_SEPARATION_CHAR}question"       <-----------
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

CLASS_REQUIREMENT_EXPLANATION = f"""
input_class is required.
Class example:

class ExampleObj:    <-------- Class example
    number: int         
    question: bool   

    NUMBER{SOURCE_SUFFIX} = "data{SOURCE_SEPARATION_CHAR}number"
    QUESTION{SOURCE_SUFFIX} = "data{SOURCE_SEPARATION_CHAR}question"

                                        Class input                               
                                            |
                                            |
model_factory = DictionaryModelFactory(ExampleObj, input_dict)
"""

ANNOTATION_FOR_SOURCES = f"""
Each source require to have a type annotation variable.

For example:

class ExampleObj:  
    number: int            <-------- annotation for the number input 
    question: bool   

    NUMBER{SOURCE_SUFFIX} = "data{SOURCE_SEPARATION_CHAR}number"     <-------- The source path for the number input
    QUESTION{SOURCE_SUFFIX} = "data{SOURCE_SEPARATION_CHAR}question"
"""
