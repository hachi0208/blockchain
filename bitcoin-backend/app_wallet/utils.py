import collections
import logging
import re

logger = logging.getLogger(__name__)

RE_IP = re.compile(
    '(?P<prefix_host>^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.)'
    '(?P<last_ip>\\d{1,3}$)')


def sorted_dict_by_key(unsorted_dict):
    return collections.OrderedDict(
        sorted(unsorted_dict.items(), key=lambda d: d[0]))