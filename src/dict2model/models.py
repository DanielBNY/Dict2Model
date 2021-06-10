class MetaModel(type):
    def __new__(cls, name, bases, dct):
        x = super().__new__(cls, name, bases, dct)
        return x

    def source(cls, path: list, disable_type_exception=False,
               disable_path_exception=False) -> object:
        setattr(cls, 'path', path)
        setattr(cls, 'disable_type_exception', disable_type_exception)
        setattr(cls, 'disable_path_exception', disable_path_exception)
        return


class Dict(metaclass=MetaModel):
    def get_path(self):
        return getattr(self, 'path')


class Example(Dict):
    a: int = Dict.source(path=['g', 'a'])
    b: str = Dict.source(path=['j', 'a'])


b = Example()
print(b.get_path())
