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

    def source(cls, path: list, type: type, disable_type_exception=False,
               disable_path_exception=False) -> object:
        new_source_info = SourceInfo(path=path, disable_path_exception=disable_path_exception,
                                     disable_type_exception=disable_type_exception, required_type=type)
        source_info_obj_dict = cls.get_source_info_obj_dict()
        source_info_obj_dict.__setitem__(hash(new_source_info), new_source_info)
        setattr(cls, SOURCE_INFO_KEY, source_info_obj_dict)
        return hash(new_source_info)


class Dict2Model(metaclass=MetaModel):
    pass


class Factory:
    def __init__(self, model: object, dictionary: dict):
        self.source_info_obj_dict = getattr(model, SOURCE_INFO_KEY)
        self.indexed_attributes = {}
        self.save_indexed_attributes(model.__dict__)

    def save_indexed_attributes(self, model_dict):
        for key in model_dict:
            if isinstance(model_dict.get(key), int):
                if model_dict.get(key) in self.source_info_obj_dict:
                    variable_name = key
                    source_info_hash = model_dict[key]
                    self.indexed_attributes[source_info_hash] = variable_name


class Example(Dict2Model):
    a: int = Dict2Model.source(path=['g', 'a'], type=int)
    b: str = Dict2Model.source(path=['j', 'a'], type=str)


f = Factory(Example, {'a': 3})
print(f.__dict__)
