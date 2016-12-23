# from cgi import parse_qs


# def application(env, start_response):
#    start_response('200_OK', [('Content-Type', 'text/html')])
#    result = []
#    result.append("Hello, world!<br><br>\n\n")
#    qs = parse_qs(env['QUERY_STRING'])
#    for k in qs:
#        result.append( str(k) + " = " + str(qs[k][0]) + "<br>\n")
#    return result
