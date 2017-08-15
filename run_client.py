#!/usr/bin/env python

from insights.client.config import compile_config, CONFIG as config
from insights.client import InsightsClient
from insights.client.client import set_up_logging, handle_startup


def main():
    compile_config()
    set_up_logging()
    v = handle_startup()
    if v is not None:
        if type(v) != bool:
            print v
        return
    else:
        client = InsightsClient()
        tar = client.collect(check_timestamp=False)
        if not config['no_upload']:
            client.upload(tar)
        else:
            print tar


if __name__ == "__main__":
    main()
