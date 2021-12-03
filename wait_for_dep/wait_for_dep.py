import importlib
import sys
import time
import re
from urllib.parse import urlparse
import argparse

scheme_type = r"[a-z0-9]+"

class WaitForDep:
    def __init__(self, check_interval=1):
        self.check_interval = check_interval

    def wait(self, url):
        parsed_url = urlparse(url)
        scheme_parsed = parsed_url.scheme.lower()
        scheme = re.match(scheme_type,scheme_parsed).group()
        
        url_no_password = (
            url.replace(parsed_url.password, "*****") if parsed_url.password else url
        )

        try:
            module_name = f"wait_for_dep.checks.{scheme}"
            check_module = importlib.import_module(module_name)
            check = check_module.check
        except ImportError:
            print(
                "Unsupported scheme: {} in url: {}".format(scheme, url_no_password)
            )
            if parsed_url.port:                
                print("Using TCP for url: {}".format(url_no_password))
                module_name = f"wait_for_dep.checks.tcp"
                check_module = importlib.import_module(module_name)
                check = check_module.check
            else:
                print("Unknown URL scheme without port exiting: {}".format(url_no_password))                
                time.sleep(self.check_interval)
                exit(0)

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
    
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('urls', metavar='N', type=str, nargs='+',
                        help='space seperated list of urls to check')
    
    args = parser.parse_args()
    urls = args.urls
    
    for url in urls:
        if not url == "":
            w.wait(url)


if __name__ == "__main__":
    main()
