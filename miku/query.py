from typing import Any, Dict, List, Optional

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
    def __init__(self, type: str, *, name: Optional[str] = None, variables: Optional[Dict[str, str]] = None) -> None:
        self.name = name
        self.type = type
        self.variables = variables or {}

    def build(self):
        vars = ', '.join([f'{k}: {v}' for k, v in self.variables.items()])

        if self.name:
            operation = f'{self.type} {self.name}'
        else:
            operation = f'{self.type}'

        if self.variables:
            operation += f'({vars})'

        return operation + ' {'

    def __str__(self) -> str:
        return  self.build()

class QueryField:
    def __init__(self, name: str, *items: str, **arguments: Any) -> None:
        self.name = name
        self.arguments = arguments
        self.items = list(items)
        self.fields: List[QueryField] = []

    def __repr__(self) -> str:
        return f'<QueryField name={self.name!r}>'

    def add_field(self, name: str, *items: str, **arguments: Any):
        field = QueryField(name, *items, **arguments)
        self.fields.append(field)

        return field

    def build(self):
        args = ', '.join([f'{k}: {v}' for k, v in self.arguments.items()])
        fields = ' '.join([field.build() for field in self.fields])
        items = ' '.join(self.items)

        query = self.name
        if self.arguments:
            query += f' ({args})'

        if self.fields:
            query += ' { ' + fields + ' }'
        elif self.items:
            query += ' { ' + items + ' }'
        elif self.items and self.fields:
            query += ' { ' + fields + items + ' }'

        return query

    def __str__(self) -> str:
        return self.build()

class QueryFields:
    def __init__(self, name: str, fields: Optional[List[QueryField]] = None, **arguments: Any) -> None:
        self.name = name
        self.fields = fields or []
        self.arguments = arguments

    def add_field(self, name: str, *items: str, **arguments: Any):
        field = QueryField(name, *items, **arguments)
        self.fields.append(field)

        return field
    
    def build(self):
        fields = ' '.join([field.build() for field in self.fields])
        args = ', '.join([f'{k}: {v}' for k, v in self.arguments.items()])

        query = f'{self.name}'
        if self.arguments:
            query += f'({args}) '

        if fields:
            query +=  '{ ' + fields + ' }'

        return query

    def __str__(self) -> str:
        return self.build()

class Query:
    def __init__(self, *, operation: Optional[QueryOperation] = None, fields: Optional[QueryFields] = None) -> None:
        self._operation = operation
        self._fields = fields

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, value: QueryOperation):
        if not isinstance(value, QueryOperation):
            raise TypeError('operation value must be an instance of QueryOperation')

        self._operation = value

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, value: QueryFields):
        if not isinstance(value, QueryFields):
            raise TypeError('fields value must be an instance of QueryFields')

        self._fields = value

    def set_operation(self, type: str, *, name: Optional[str] = None, variables: Dict[str, str]):
        operation = QueryOperation(type, name=name, variables=variables)
        self._operation = operation

        return operation
    
    def add_fields(self, name: str, fields: Optional[List[QueryField]] = None, **arguments) -> QueryFields:
        self.fields = QueryFields(name, fields, **arguments)
        return self.fields

    def build(self) -> str:
        if not self.operation or not self.fields:
            raise QueryIncomplete('operation')

        operation = self.operation.build()

        query = operation + ' '
        query += self.fields.build()

        return query + ' }'

    def __str__(self) -> str:
        return self.build()
