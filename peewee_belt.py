# -*- coding: utf-8 -*-
from pprint import pprint

import peewee as pw
import schematics as sc
from schematics import types

_fields_map = {
    pw.AutoField: types.IntType,
    pw.CharField: types.StringType,
    pw.SmallIntegerField: types.IntType
}


class ValidatorMeta(pw.ModelBase):
    def __new__(cls, name, bases, attrs):
        print(name, bases, attrs)
        cls = super(ValidatorMeta, cls).__new__(cls, name, bases, attrs)
        print(cls, cls.__dict__, '呵, 女人', )

        validator_attrs = {}
        for field in cls._meta.sorted_fields:
            print(field)
            f = _fields_map.get(field.__class__, types.BaseType)
            params = {
                'required': not field.null
            }
            validator_attrs[field.name] = f(**params)
        # key = field.name
        #
        # cls._schema.append_field(schema.Field(key, f(**params)))
        # setattr(cls, key, models.FieldDescriptor(key))
        validator = type(name + 'Validator', (sc.Model,), validator_attrs)

        cls.validator = validator

        def validate(self):
            self.validator(self.__data__).validate()

        cls.validate = validate

        return cls


class Model(pw.Model, metaclass=ValidatorMeta):
    title = pw.CharField(max_length=45, unique=True)
    difficulty = pw.SmallIntegerField()


pprint(Model.validator.__dict__)

m = Model(title='呵, 男人👱', id=10, difficulty='asd')
m.validate()

vm = m.validator(m.__data__)
print(vm.to_primitive())
