from typing import Dict, List, Optional, Tuple

__all__ = (
    'QueryIncomplete',
    'QueryOperation',
    'QueryFields',
    'QueryField',
    'Query'
)

class QueryIncomplete(Exception):
    def __init__(self, element: str) -> None:
        super().__init__(f'Query missing {element!r} element')

class QueryOperation:
    def __init__(self, type: str, *, name: str=None, variables: Dict[str, str]) -> None:
        self.name = name
        self.type = type
        self.variables = variables

    def build(self):
        vars = ', '.join([f'{k}: {v}' for k, v in self.variables.items()])

        if self.name:
            operation = f'{self.type} {self.name} ({vars}) '
        else:
            operation = f'{self.type} ({vars}) '

        return operation + '{'

    def __str__(self) -> str:
        return  self.build()

class QueryField:
    def __init__(self, name: str, *items, **arguments) -> None:
        self.name = name
        self.arguments = arguments

        self._items = list(items)
        self.fields = []

    def add_item(self, name: str):
        self._items.append(name)
        return self

    def add_items(self, *names):
        self._items.extend(list(names))
        return self

    def add_field(self, name: str, *items, **arguments):
        field = QueryField(name, *items, **arguments)
        self.fields.append(field)

        return field

    def build(self):
        args = ', '.join([f'{k}: {v}' for k, v in self.arguments.items()])
        fields = '\n'.join([field.build() for field in self.fields])
        items = '\n'.join(self._items)

        if self._items or self.arguments:
            if args:
                query = f'{self.name} ({args}) ' + '{\n' + f'{fields}\n{items}' + '\n}' 
            else:
                query = f'{self.name} ' + '{\n' + f'{fields}\n{items}' + '\n}' 

            return query

        return self.name

    def __str__(self) -> str:
        return self.build()

class QueryFields:
    def __init__(self, name: str, fields: List[QueryField]=None, **arguments) -> None:
        self.name = name
        self.fields = fields or []

        self.arguments = arguments

    def add_field(self, name: str, *items: Tuple[str], **arguments):
        field = QueryField(name, *items, **arguments)
        self.fields.append(field)

        return field
    
    def build(self):
        if not self.fields:
            raise QueryIncomplete('fields')

        fields = '\n'.join([field.build() for field in self.fields])
        args = ', '.join([f'{k}: {v}' for k, v in self.arguments.items()])

        query = f'{self.name} ({args}) ' + '{\n' + fields + '\n}'
        return query

    def __str__(self) -> str:
        return self.build()

class Query:
    def __init__(self, operation: QueryOperation=None, fields: QueryFields=None) -> None:
        self._opration: Optional[QueryOperation] = operation
        self._fields = fields

    @property
    def operation(self):
        return self._opration

    @operation.setter
    def operation(self, value):
        if not isinstance(value, QueryOperation):
            raise TypeError('operation value must be an instance of QueryOperation')

        self._opration = value

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, value):
        if not isinstance(value, QueryFields):
            raise TypeError('fields value must be an instance of QueryFields')

        self._fields = value

    def set_operation(self, type: str, *, name: str=None, variables: Dict[str, str]):
        operation = QueryOperation(type, name=name, variables=variables)
        self._opration = operation

        return operation
    
    def add_fields(self, name: str, fields: List[QueryField]=None, **arguments) -> QueryFields:
        fields = QueryFields(name, fields, **arguments)
        self._fields = fields

        return fields

    def build(self) -> str:
        if not self._opration:
            raise QueryIncomplete('operation')

        operation = self.operation.build()

        query = operation + ' '
        query += self.fields.build()

        return query + '\n}'

    def __str__(self) -> str:
        return self.build()
