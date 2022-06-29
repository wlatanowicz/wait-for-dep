import argparse
import importlib
import sys
import time
from urllib.parse import urlparse
from itertools import count


class WaitForDep:
    def __init__(self, check_interval, timeout):
        self.check_interval = check_interval
        self.timeout = timeout

    def wait(self, url):
        parsed_url = urlparse(url)
        scheme = parsed_url.scheme

        url_no_password = (
            url.replace(parsed_url.password, "*****") if parsed_url.password else url
        )

        try:
            module_name = f"wait_for_dep.checks.{scheme}"
            check_module = importlib.import_module(module_name)
            check = check_module.check
        except ImportError:
            print("Unsupported scheme: {} in url: {}".format(scheme, url_no_password))
            print("Using TCP for url: {}".format(url_no_password))
            module_name = f"wait_for_dep.checks.tcp"
            check_module = importlib.import_module(module_name)
            check = check_module.check

        last_message = 0
        message_interval = 20
        for i in count():
            connected = check(url)
            if connected:
                break

            elapsed = i * self.check_interval

            if self.timeout is not None and elapsed >= self.timeout:
                print("Can't connect to {}. Exiting.".format(url_no_password))
                sys.exit(1)

            if i == 0:
                print("Waiting for {}".format(url_no_password))
            elif elapsed >= last_message + message_interval:
                print(
                    "Still waiting for {} ({}s elapsed)".format(
                        url_no_password, elapsed
                    )
                )
                last_message = elapsed

            time.sleep(self.check_interval)

        print("Successfully connected to {}".format(url_no_password))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=int, default=1, help="Delay between checks")
    parser.add_argument(
        "--timeout", type=int, help="Time out in seconds for single dependency check"
    )
    parser.add_argument(
        "urls", type=str, nargs="*", help="URL of the dependency resource"
    )

    args = parser.parse_args()

    w = WaitForDep(
        check_interval=args.interval,
        timeout=args.timeout,
    )

    for url in args.urls:
        w.wait(url)


if __name__ == "__main__":
    main()
