from dataclasses import dataclass
from settings import data


@dataclass
class Host:
    host: str
    check_text: str
    check_times: str
    check_period_sec: int
    check_error: int


def hosts():
    host_list = []
    for host in data:
        h = Host(
            host["host"],
            host["check_text"],
            host["check_times"],
            host["check_period_sec"],
            0,
        )
        host_list.append(h)
    return host_list
