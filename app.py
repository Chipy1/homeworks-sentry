import os
import random
import time

import sentry_sdk

DSN = os.environ["SENTRY_DSN"]

sentry_sdk.init(
    dsn=DSN,
    traces_sample_rate=1.0,
    environment="local",
    release="homework@1.0.0",
)


def divide(a, b):
    return a / b


def main():
    print("sending events...")
    try:
        raise ValueError("User is too young")
    except Exception:
        sentry_sdk.capture_exception()

    try:
        divide(10, 0)
    except ZeroDivisionError:
        sentry_sdk.capture_message("division by zero in divide()", level="error")

    sentry_sdk.capture_message("just a warning for the alert", level="warning")
    with sentry_sdk.configure_scope() as scope:
        scope.set_tag("homework", "monitoring-05")
        scope.set_user({"id": str(random.randint(1, 9999)), "email": "tester@local.dev"})
        sentry_sdk.capture_message("message with custom tags and user")

    print("done, waiting for flush...")
    time.sleep(2)
    sentry_sdk.flush()


if __name__ == "__main__":
    main()