import functools
import time
import app.databaseUtil as databaseUtil 
import psycopg2 


def Log(message,info):
    try:
        databaseUtil.insertQuery(f"call log('{message}','{info}')")
    except:
        pass


def databaseError(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):

        try:
            func(*args,**kwargs)

        except psycopg2.OperationalError as error:
            Log(f"{func.__name__}  :  f{error}","error")

        except psycopg2.NotSupportedError as error:
            Log(f"{func.__name__}  :  f{error}","error")

        except psycopg2.ProgrammingError as error:
            Log(f"{func.__name__}  : f{error}","error")

        except psycopg2.InternalError as error:
            Log(f"{func.__name__}  : f{error}","error")    

        except psycopg2.DatabaseError as error:
            Log(f"{func.__name__}  : f{error}","error")

    return wrapper


def any_error(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        try:
            func(*args,**kwargs)

        except Exception as error:
            Log(f"{func.__name__}  : f{error}", "error")

    return wrapper


def timer(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):

        start_time = time.perf_counter()
        func(*args,**kwargs)
        finish_time = time.perf_counter()

        run_time = finish_time - start_time

        Log(f"Fonksiyon İsmi {func.__name__} , çalışma zamanı = {run_time:0.4f} saniye","info")

    return wrapper
