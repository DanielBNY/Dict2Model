SOURCE_INFO_KEY = '__source_info_obj_dict__'


class SourceInfo:
    def __init__(self, path, type_exception, path_exception, required_type):
        self.path = path
        self.type_exception = type_exception
        self.path_exception = path_exception
        self.type = required_type


class MetaModel(type):
    def __get__(cls, attribute):
        try:
            value = getattr(cls, attribute)
            return value
        except AttributeError:
            return None

    def _get_source_info_obj_dict(cls):
        source_info_obj_dict = cls.__get__(SOURCE_INFO_KEY)
        if source_info_obj_dict is None:
            return {}
        return source_info_obj_dict

    def source(cls, path, required_type, type_exception=True,
               path_exception=True):
        cls._validate_source_input(path, required_type, type_exception, path_exception)
        new_source_info = SourceInfo(path=path, path_exception=path_exception,
                                     type_exception=type_exception, required_type=required_type)
        source_info_obj_dict = cls._get_source_info_obj_dict()
        source_info_obj_dict.__setitem__(hash(new_source_info), new_source_info)
        setattr(cls, SOURCE_INFO_KEY, source_info_obj_dict)
        return hash(new_source_info)

    def _validate_source_input(cls, path, required_type, type_exception, path_exception):
        cls._validate_list_type(path, str)
        cls._validate_required_type(required_type)
        cls._validate_exception_condition(type_exception, path_exception)

    @staticmethod
    def _validate_exception_condition(type_exception, path_exception):
        if not isinstance(type_exception, bool) or \
                not isinstance(path_exception, bool):
            raise TypeError

    @staticmethod
    def _validate_required_type(required_type):
        if not isinstance(required_type, type):
            raise TypeError

    @staticmethod
    def _validate_list_type(list_to_validate, type_to_validate):
        for item in list_to_validate:
            if not isinstance(item, type_to_validate):
                raise TypeError


class Dict2Model(metaclass=MetaModel):
    log = ''


class ModelFactory:
    def __init__(self, model_class):
        self._validate_model(model_class)
        self.dictionary_input = {}
        self.indexed_attributes = {}
        self.model_instance = model_class()
        self.source_info_obj_dict = getattr(self.model_instance, SOURCE_INFO_KEY)

    @staticmethod
    def _validate_model(model):
        if not isinstance(model, MetaModel):
            raise TypeError

    def use(self, dictionary):
        self.dictionary_input = dictionary
        self._save_indexed_attributes()
        self._set_attributes()
        return self.model_instance

    def _save_indexed_attributes(self):
        for key in dir(self.model_instance):
            value = getattr(self.model_instance, key)
            if isinstance(value, int):
                if value in self.source_info_obj_dict:
                    variable_name = key
                    source_info_hash = value
                    self.indexed_attributes[source_info_hash] = variable_name

    def _set_attributes(self):
        keys = self.source_info_obj_dict.keys()
        print(self.indexed_attributes)
        for key in keys:
            source_onj = self.source_info_obj_dict[key]
            variable_input = self._get_input_from_source(source_onj.path, source_onj.path_exception)
            if isinstance(variable_input, source_onj.type):
                setattr(self.model_instance, self.indexed_attributes[key], variable_input)
            else:
                if source_onj.type_exception:
                    raise Exception
                else:
                    setattr(self.model_instance, self.indexed_attributes[key], None)

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


example2 = ModelFactory(Example).use({'a': 3, 'j': 3})
print(example2.a, example2.b)
print(Example.__dict__)
print(example2)
