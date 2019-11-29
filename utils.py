from typing import Optional, List, Tuple, Dict

from mock_types import QueryString, HttpRequest


def join_query_string(qs: Optional[List[QueryString]]):
    if qs is None:
        return ''
    joined_values = dict(sorted({x.name: ",".join(sorted(x.values)) for x in qs}.items()))
    return '&'.join([f'{key}={value}' for key, value in joined_values.items()])


def request_hash(request: HttpRequest):
    qs = join_query_string(request.query_string_parameters)
    return f'{request.method}:{request.path}?{qs}'


def query_params_to_http_qs(qs: List[Tuple[str, str]]):
    query_params: Dict[str, List[str]] = {}
    for param in qs:
        qp = query_params.get(param[0])
        if qp:
            qp.append(param[1])
        else:
            query_params[param[0]] = [param[1]]
    query_string: List[QueryString] = []
    for key, value in query_params.items():
        query_string.append(QueryString(name=key, values=value))
    return query_string
