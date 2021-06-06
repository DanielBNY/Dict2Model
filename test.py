from src.dict2model import Dict2Model


class TestObj:
    number: int
    question: bool

    NUMBER_SOURCE = "data-number"
    QUESTION_SOURCE = "data-question"
    DISABLE_TYPE_EXCEPTIONS = True
    DISABLE_PATH_EXCEPTIONS = True


dict_input_test = {
    "data": {
        "number": 123,
        "question": True
    }
}

factory = Dict2Model.Dict2Model(TestObj, dict_input_test)
test_obj: TestObj = factory.run()
print(test_obj.number, test_obj.question)
print(type(test_obj.number), type(test_obj.question))
