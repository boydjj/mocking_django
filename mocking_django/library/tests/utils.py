def render_to_response_echo(*args, **kwargs):
    """
    Replacement render_to_response that records the context and template args.
    Modified version of pattern cribbed from the Internets at
    http://chase-seibert.github.io/blog/2012/07/27/faster-django-view-unit-tests-with-mocks.html
    """
    res = dict(template_name=args[0])

    if len(args) > 1:
        res['context'] = args[1].dicts[0]

    return res
