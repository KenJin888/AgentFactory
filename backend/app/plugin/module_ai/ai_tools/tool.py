import inspect

from fastapi import Query


def get_init_params(cls):
    """返回类 __init__ 方法的参数信息（不含 self）"""
    sig = inspect.signature(cls.__init__)
    params = {}
    for name, param in sig.parameters.items():
        if name == 'self':
            continue
        # 参数信息：kind（位置/关键字等）、默认值（如果没有则为空）
        params[name] = {
            'kind': param.kind,
            'default': param.default if param.default is not param.empty else None,
            'annotation': param.annotation if param.annotation is not param.empty else None,
        }
    return params


def get_cls_object(cls, data):
    cls_params = get_init_params(cls)
    init_params = {}
    for key, value in cls_params.items():
        if data.get(key):
            default = data.get(key)
        elif type(value['default']) == type(Query()):
            default = value['default'].default
        else:
            default = value['default']
        init_params[key] = default
    return cls(**init_params)