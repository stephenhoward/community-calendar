import sys
import re

def query_from_query_string(cls,**parameters):
    query  = cls.query
    joins  = {}

    for param in parameters:

        model_class = cls
        value       = parameters[param]

        rel_name, model_attr, operator = _parse_parameter( param )

        if rel_name:
            rel_class = getattr( cls, rel_name ).property.mapper.class_

            if rel_class.__name__ not in joins:
                query = query.join(rel_class)
                joins[ rel_class.__name__ ] = 1

            model_class = rel_class

        query = query.filter( _operator_map[ operator ]( getattr(model_class,model_attr), value ) )

    return query

class QueryFormatException (Exception):

    def __init__(self,message):
        self.message = message

query_format = re.compile("^  ( (?:\w+\.)? \w+)   (?: \[  (.+?)  \] )?   $", re.X)
join_format  = re.compile("^ (\w+) \. (\w+) $", re.X)

def _parse_parameter(param):
    rel_name = None
    model_attr = param
    operator = 'eq'

    query_match = query_format.match( param )
    if query_match:

        if query_match.group(2):
            operator = query_match.group(2)

        join_match = join_format.match( query_match.group(1) )

        if join_match:
            rel_name  = join_match.group(1)
            rel_attr  = join_match.group(2)
        else:
            rel_attr = query_match.group(1)

    else:
        raise QueryFormatException("bad query format: " + param )

    return ( rel_name, rel_attr, operator )

_operator_map = {
    'ne': ( lambda k,v: ( k != v ) ),
    'eq': ( lambda k,v: ( k == v ) ),
    'gt': ( lambda k,v: ( k > v  ) ),
    'ge': ( lambda k,v: ( k >= v ) ),
    'lt': ( lambda k,v: ( k < v  ) ),
    'le': ( lambda k,v: ( k <= v ) ),
}