from DictionaryModel import DictionaryModel


class TestObj:
    number: int
    question: bool

    NUMBER_SOURCE = "data-number"  # dict source
    QUESTION_SOURCE = "data-question"  # dict source
    DISABLE_TYPE_EXCEPTIONS = True


dict_input_test = {
    "data": {
        "number": 123,
        "question": True
    }
}


def test():
    test_obj: TestObj = DictionaryModel(TestObj, dict_input_test).run()
    print(test_obj.number, test_obj.question)
test()