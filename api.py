# api.py
from fastapi import APIRouter, Depends
from models import PowRequest, FibRequest, FactRequest
from services import calculate_pow, fibonacci, factorial
from worker import task_queue
from db import log_request
from auth import verify_token
from cache import get_cached_result, set_cached_result


router = APIRouter()


@router.post("/power")
def power(req: PowRequest, user=Depends(verify_token)):
    result = calculate_pow(req.base, req.exponent)
    task_queue.put({
        "func": log_request,
        "args": ("power", req.json(), str(result))
    })
    return {"user": user, "result": result}


@router.post("/fib")
def fib(req: FibRequest, user=Depends(verify_token)):
    cache_key = f"fib:{req.n}"
    cached = get_cached_result(cache_key)
    if cached is not None:
        return {"user": user, "result": cached, "cached": True}

    result = fibonacci(req.n)
    set_cached_result(cache_key, result)
    task_queue.put({
        "func": log_request,
        "args": ("fibonacci", req.json(), str(result))
    })
    return {"user": user, "result": result, "cached": False}


@router.post("/fact")
def fact(req: FactRequest, user=Depends(verify_token)):
    cache_key = f"fact:{req.n}"
    cached = get_cached_result(cache_key)
    if cached is not None:
        return {"user": user, "result": cached, "cached": True}

    result = factorial(req.n)
    set_cached_result(cache_key, result)
    task_queue.put({
        "func": log_request,
        "args": ("factorial", req.json(), str(result))
    })
    return {"user": user, "result": result, "cached": False}
