from math import ceil
from typing import NoReturn

from fastapi import Request, Response
from app.core.exceptions import CustomException

def http_limit_callback(request: Request, response: Response, expire: int) -> NoReturn:
    """
    请求限制时的默认回调函数

    :param request: FastAPI 请求对象
    :param response: FastAPI 响应对象
    :param expire: 剩余毫秒数
    :return:
    """
    expires = ceil(expire / 30)
    raise CustomException(
        status_code=429,
        msg="请求过于频繁，请稍后重试！",
        data={"Retry-After": str(expires)},
    )

