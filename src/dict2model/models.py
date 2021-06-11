SOURCE_INFO_KEY = 'source_info_obj_dict'


class SourceInfo:
    def __init__(self, path: list, disable_type_exception: bool, disable_path_exception: bool):
        self.path = path
        self.disable_type_exception = disable_type_exception
        self.disable_path_exception = disable_path_exception


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

    def source(cls, path: list, disable_type_exception=False,
               disable_path_exception=False) -> object:
        new_source_info = SourceInfo(path=path, disable_path_exception=disable_path_exception,
                                     disable_type_exception=disable_type_exception)
        source_info_obj_dict = cls.get_source_info_obj_dict()
        source_info_obj_dict.__setitem__(hash(new_source_info), new_source_info)
        setattr(cls, SOURCE_INFO_KEY, source_info_obj_dict)
        return hash(new_source_info)


class Model(metaclass=MetaModel):
    def get_path(self):
        return getattr(self, SOURCE_INFO_KEY)


class Example(Model):
    a: int = Model.source(path=['g', 'a'])
    b: str = Model.source(path=['j', 'a'])


b = Example()
print(b.a, b.b, b.get_path())
