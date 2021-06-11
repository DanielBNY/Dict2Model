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

    def get_source_info_obj_list(cls) -> list:
        source_info_obj_list = cls.__get__('source_info_obj_list')
        if not source_info_obj_list:
            return []
        return source_info_obj_list

    def source(cls, path: list, disable_type_exception=False,
               disable_path_exception=False) -> object:
        new_source_info = SourceInfo(path=path, disable_path_exception=disable_path_exception,
                                     disable_type_exception=disable_type_exception)
        source_info_obj_list = cls.get_source_info_obj_list()
        source_info_obj_list.append(new_source_info)
        setattr(cls, 'source_info_obj_list', source_info_obj_list)
        return


class Model(metaclass=MetaModel):
    def get_path(self):
        return getattr(self, 'source_info_obj_list')


class Example(Model):
    a: int = Model.source(path=['g', 'a'])
    b: str = Model.source(path=['j', 'a'])


b = Example()
print(b.get_path())
