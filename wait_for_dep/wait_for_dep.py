import importlib
import sys
import time
from urllib.parse import urlparse


class WaitForDep:
    def __init__(self, check_interval=1):
        self.check_interval = check_interval

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
            raise ValueError(
                "Unsupported scheme: {} in url: {}".format(scheme, url_no_password)
            )

        i = 0
        while True:
            connected = check(url)
            if connected:
                break

            if i % 20 == 0:
                if i > 0:
                    sec = i * self.check_interval
                    print(
                        "Still waiting for {} ({}s elapsed)".format(
                            url_no_password, sec
                        )
                    )
                else:
                    print("Waiting for {}".format(url_no_password))
            i += 1

            time.sleep(self.check_interval)

        print("Successfully connected to {}".format(url_no_password))


def main():
    w = WaitForDep()
    args = sys.argv
    args.pop(0)

    for url in args:
        w.wait(url)


if __name__ == "__main__":
    main()
