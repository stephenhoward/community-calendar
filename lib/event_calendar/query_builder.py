import re
from sqlalchemy.inspection import inspect

query_format = re.compile("^  (\w+)   \[  (.+?)  \]   $", re.X)

def from_query_string(cls,**parameters):
    query  = []

    for param in parameters:
        match = query_format.match( param )
        if match:
            query.append( _operator_map[ match.group(2) ]( getattr(cls,match.group(1)), parameters[param] ) )
        else:
            query.append( getattr(cls,param)  == parameters[param] )

    return query


_operator_map = {
    'gt': ( lambda k,v: ( k > v  ) ),
    'ge': ( lambda k,v: ( k >= v ) ),
    'lt': ( lambda k,v: ( k < v  ) ),
    'le': ( lambda k,v: ( k <= v ) ),
}