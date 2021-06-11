SOURCE_INFO_KEY = 'source_info_obj_dict'


class SourceInfo:
    def __init__(self, path: list, type_exception: bool, path_exception: bool, required_type: type):
        self.path = path
        self.type_exception = type_exception
        self.path_exception = path_exception
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

    def source(cls, path: list, required_type: type, type_exception=True,
               path_exception=True) -> object:
        cls.validate_source_input(path, required_type, type_exception, path_exception)
        new_source_info = SourceInfo(path=path, path_exception=path_exception,
                                     type_exception=type_exception, required_type=required_type)
        source_info_obj_dict = cls.get_source_info_obj_dict()
        source_info_obj_dict.__setitem__(hash(new_source_info), new_source_info)
        setattr(cls, SOURCE_INFO_KEY, source_info_obj_dict)
        return hash(new_source_info)

    def validate_source_input(cls, path, required_type, type_exception, path_exception):
        cls.validate_list_type(path, str)

    @staticmethod
    def validate_list_type(list_to_validate, type_to_validate):
        for item in list_to_validate:
            if not isinstance(item, type_to_validate):
                raise TypeError


class Dict2Model(metaclass=MetaModel):
    pass


class Factory:
    def __init__(self, model):
        self.dictionary_input = {}
        self.indexed_attributes = {}
        self.model = model()
        self.source_info_obj_dict = getattr(self.model, SOURCE_INFO_KEY)

    def run(self, dictionary):
        self.dictionary_input = dictionary
        self.save_indexed_attributes()
        self.set_attributes()
        return self.model

    def save_indexed_attributes(self):
        for key in dir(self.model):
            value = getattr(self.model, key)
            if isinstance(value, int):
                if value in self.source_info_obj_dict:
                    variable_name = key
                    source_info_hash = value
                    self.indexed_attributes[source_info_hash] = variable_name

    def set_attributes(self):
        keys = self.source_info_obj_dict.keys()
        print(self.indexed_attributes)
        for key in keys:
            source_onj = self.source_info_obj_dict[key]
            variable_input = self._get_input_from_source(source_onj.path, source_onj.path_exception)
            if isinstance(variable_input, source_onj.type):
                setattr(self.model, self.indexed_attributes[key], variable_input)
            else:
                if source_onj.type_exception:
                    raise Exception
                else:
                    setattr(self.model, self.indexed_attributes[key], None)

    def _get_input_from_source(self, dictionary_path, path_exception):
        data = self.dictionary_input
        for key in dictionary_path:
            if data and isinstance(data, dict):
                data = data.get(key)
            else:
                if path_exception:
                    raise Exception
                else:
                    return None
        return data


class Example(Dict2Model):
    a = Dict2Model.source(path=['random'], required_type=int, type_exception=False, path_exception=False)
    b = Dict2Model.source(path=['j'], required_type=int, type_exception=False, path_exception=False)


factory = Factory(Example)
example2: Example = factory.run({'a': 3, 'j': 3})
print(example2.a, example2.b)
print(Example.__dict__)
