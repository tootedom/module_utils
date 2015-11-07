#!/usr/bin/env python

import time


aws_retry_api_throlling_retries = 10


class RetryLimitExceeded(Exception):
    def __init__(self, exception, retries):
        self.exception = exception
        self.tries = retries

    def __str__(self):
        return repr(
            "Throttling retry limit exceeded, no_of_tries({0}), last exception: {1}".format(self.tries, self.exception))


def get_api_error_code(exception):
    if hasattr(exception, "body"):
        if exception.body is not None and hasattr(exception.body, "split"):
            code = exception.body.split("<Code>")[1]
            code = code.split("</Code>")[0]
            return code
        else:
            return ""
    else:
        return ""


def call_with_retry(api_call, *args, **kwargs):
    last_exception = ""
    tries = 0
    retry_interval = 2
    retry = aws_retry_api_throlling_retries
    while True:
        tries += 1
        try:
            return api_call(*args, **kwargs)
        except Exception, e:
            last_exception = e
            code = get_api_error_code(e)
            if retry <= 0:
                raise RetryLimitExceeded(last_exception, tries)
            elif retry > 0 and (code == "Throttling" or code == "RequestLimitExceeded"):
                retry -= 1
                retry_interval += 1
                time.sleep(retry_interval)
            else:
                raise e
    return None
