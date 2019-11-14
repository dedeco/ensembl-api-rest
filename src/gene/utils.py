from marshmallow import ValidationError


def min_length(length):
    def validate(s):
        if len(s) >= length:
            return s
        raise ValidationError("String must be at least %i characters long" % min)

    return validate


def get_paginated_list(gene_schema, results, url, parameters, start, limit):
    start = int(start)
    limit = int(limit)
    count = len(results)

    obj = {'start': start, 'limit': limit, 'count': count}

    if count < start or limit < 0:
        obj['results'] = []
        return obj
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + \
                          '?start=%d&limit=%d' % (start_copy, limit_copy) \
                          + '&' + parameters
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + \
                      '?start=%d&limit=%d' % (start_copy, limit) \
                      + '&' + parameters
    obj['results'] = gene_schema.dump(results[(start - 1):(start - 1 + limit)])

    return obj


def get_parameters_url(args):
    parameters = '&'.join([str(k) + '=' + str(v) for k, v in args.items() \
                           if k in ['lookup', 'species'] and v])
    return parameters


def get_parsed_parameters(parser):
    parser. \
        add_argument('lookup',
                     type=min_length(3),
                     required=True,
                     help='The partial query for gene name typed by the user, e.g. brc. Submitted parameter '
                          'must not be under 3 chars.')
    parser. \
        add_argument('species',
                     type=min_length(3),
                     help='The name of the target species, e.g. homo_sapiens. Submitted parameter must not be '
                          'under 3 chars')
    parser. \
        add_argument('start',
                     type=int,
                     default=1,
                     help='Pagination control: the response start from N records.')
    parser. \
        add_argument('limit',
                     type=int,
                     default=25,
                     help='Pagination control: limit the response in N records.')
    args = parser.parse_args()
    return args
