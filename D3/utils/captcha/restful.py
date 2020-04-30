from django.http import JsonResponse

class httpCode(object):
    ok = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500


def httpResult(code=httpCode.ok, message="", data=None, kwargs=None):
    json_data = {"code": code, "message": message, "data": data}

    # 判断是否传递了kwargs(其他的值，是否为字典类型，并且kwargs是否有值)
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_data.update(kwargs)
    return JsonResponse(json_data)

def ok():
    return httpResult()


def params_error(message="", data=None):
    return httpResult(code=httpCode.paramserror, message=message, data=data)


def unauth_error(message="", data=None):
    return httpResult(code=httpCode.unauth, message=message, data=data)


def methoderror(message="", data=None):
    return httpResult(code=httpCode.methoderror, message=message, data=data)


def servererror(message="", data=None):
    return httpResult(code=httpCode.servererror, message=message, data=data)