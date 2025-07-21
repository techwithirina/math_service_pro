# cli.py
import click
from models import PowRequest, FibRequest, FactRequest
from services import calculate_pow, fibonacci, factorial
from db import log_request, get_requests_array,  init_db


@click.group()
def cli():
    """Math Microservice CLI"""
    init_db()


@cli.command()
@click.argument('base', type=float)
@click.argument('exponent', type=float)
def power(base, exponent):
    req = PowRequest(base=base, exponent=exponent)
    result = calculate_pow(req.base, req.exponent)
    log_request('power', str(req.dict()), str(result))
    rows = get_requests_array()
    click.echo(f"Result: {result}")
    click.echo(f"Logged so far: {rows}")


@cli.command()
@click.argument('n', type=int)
def fib(n):
    req = FibRequest(n=n)
    result = fibonacci(req.n)
    log_request('fibonacci', str(req.dict()), str(result))
    rows = get_requests_array()
    click.echo(f"Fibonacci({n}) = {result}")
    click.echo(f"Logged so far: {rows}")


@cli.command()
@click.argument('n', type=int)
def fact(n):
    req = FactRequest(n=n)
    result = factorial(req.n)
    log_request('factorial', str(req.dict()), str(result))
    rows = get_requests_array()
    click.echo(f"{n}! = {result}")
    click.echo(f"Logged so far: {rows}")
