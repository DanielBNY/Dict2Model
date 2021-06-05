# SpecialModel
Special Model

![alt_text](https://raw.githubusercontent.com/DanielBNY/DictionaryModel/dev/extra/Logo.png)

The library returns an object with defined attributes in types from an input dictionary, 
with optional rules about types and more.

The declaration for the object variables and their types uses annotations:

        number: int
        question: bool

The mapping between variable and path inside the input dictionary are inside the source variables, in this format:
a string separated by '-' for each inner jump inside the dictionary
For example:

        NUMBER_SOURCE = "data-number"           # == dict_input["data"]["number"]
        QUESTION_SOURCE = "data-question"       # == dict_input["data"]["question"]

The optional parameter are:
    
    DISABLE_TYPE_EXCEPTIONS = True
    DISABLE_PATH_EXCEPTIONS = True

Type exception indicate to stop the object creation if theirs an error in matching types.
The second variable indicate to stop the object creation if a value don't exist in the source path.
When disabled variables are true the problematic variables are set to None. 
The default is DISABLE_TYPE_EXCEPTIONS and DISABLE_PATH_EXCEPTIONS as False.

Full example:

    class TestObj:
        number: int
        question: bool
        NUMBER_SOURCE = "data-number"
        QUESTION_SOURCE = "data-question"
        DISABLE_TYPE_EXCEPTIONS = True
        DISABLE_PATH_EXCEPTIONS = True


##Use

    pip install SpecialModel