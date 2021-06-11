SOURCE_INFO_KEY = 'source_info_obj_dict'


class SourceInfo:
    def __init__(self, path: list, disable_type_exception: bool, disable_path_exception: bool, required_type: type):
        self.path = path
        self.disable_type_exception = disable_type_exception
        self.disable_path_exception = disable_path_exception
        self.type = required_type


class MetaModel(type):
    def __new__(cls, name, bases, dct):
        x = super().__new__(cls, name, bases, dct)
        return x

    def __get__(cls, attribute):
        try:
            value = getattr(cls, attribute)
            return value
        except AttributeError:
            return None

    def get_source_info_obj_dict(cls) -> dict:
        source_info_obj_dict = cls.__get__(SOURCE_INFO_KEY)
        if source_info_obj_dict is None:
            return {}
        return source_info_obj_dict

    def source(cls, path: list, required_type: type, disable_type_exception=False,
               disable_path_exception=False) -> object:
        cls.validate_source_input(path, required_type, disable_type_exception, disable_path_exception)
        new_source_info = SourceInfo(path=path, disable_path_exception=disable_path_exception,
                                     disable_type_exception=disable_type_exception, required_type=required_type)
        source_info_obj_dict = cls.get_source_info_obj_dict()
        source_info_obj_dict.__setitem__(hash(new_source_info), new_source_info)
        setattr(cls, SOURCE_INFO_KEY, source_info_obj_dict)
        return hash(new_source_info)

    def validate_source_input(cls, path, required_type, disable_type_exception, disable_path_exception):
        cls.validate_list_type(path, str)

    @staticmethod
    def validate_list_type(list_to_validate, type_to_validate):
        for item in list_to_validate:
            if not isinstance(item, type_to_validate):
                raise TypeError


class Dict2Model(metaclass=MetaModel):
    pass


class Factory:
    def __init__(self, model: object, dictionary: dict):
        self.dictionary_input = dictionary
        self.source_info_obj_dict = getattr(model, SOURCE_INFO_KEY)
        self.indexed_attributes = {}
        self.save_indexed_attributes(model.__dict__)
        self.set_attributes(model)

    def save_indexed_attributes(self, model_dict):
        for key in model_dict:
            if isinstance(model_dict.get(key), int):
                if model_dict.get(key) in self.source_info_obj_dict:
                    variable_name = key
                    source_info_hash = model_dict[key]
                    self.indexed_attributes[source_info_hash] = variable_name

    def set_attributes(self, model):
        keys = self.source_info_obj_dict.keys()
        print(self.indexed_attributes)
        for key in keys:
            source_onj = self.source_info_obj_dict[key]
            variable_input = self._get_input_from_source(source_onj.path, source_onj.disable_path_exception)
            if isinstance(variable_input, source_onj.type):
                setattr(model, self.indexed_attributes[key], variable_input)
            else:
                if not source_onj.disable_type_exception:
                    raise Exception

    def _get_input_from_source(self, dictionary_path, disable_path_exception):
        data = self.dictionary_input
        for key in dictionary_path:
            if data:
                data = data.get(key)
                if data is None and not disable_path_exception:
                    raise Exception
        return data


class Example(Dict2Model):
    a = Dict2Model.source(path=['a'], required_type=int)
    b = Dict2Model.source(path=['j'], required_type=str)


example1 = Example
Factory(example1, {'a': 3, 'j': '7'})
print(example1.a, example1.b)
