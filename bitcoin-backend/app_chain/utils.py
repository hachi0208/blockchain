import collections
import logging
import re
import socket

logger = logging.getLogger(__name__)

"""
^: 文字列の開始を意味します。
\\d{1,3}: 1から3桁の数字を意味します。これは各オクテットが0から255までの値を取ることができるためです。
\\.: ピリオド（.）を意味します。正規表現内でピリオドを表すには、エスケープシーケンス（\\）が必要です。
(?P<name>pattern): 名前付きキャプチャグループです。patternに一致する部分をnameという名前で参照できるようにします。
"""
RE_IP = re.compile(
    '(?P<prefix_host>^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.)'
    '(?P<last_ip>\\d{1,3}$)')


def sorted_dict_by_key(unsorted_dict):
    return collections.OrderedDict(
        sorted(unsorted_dict.items(), key=lambda d: d[0]))


def pprint(chains):
    for i, chain in enumerate(chains):
        print(f'{"="*25} Chain {i} {"="*25}')
        for k, v in chain.items():
            if k == 'transactions':
                print(k)
                for d in v:
                    print(f'{"-"*40}')
                    for kk, vv in d.items():
                        print(f' {kk:30}{vv}')
            else:
                print(f'{k:15}{v}')
    print(f'{"*"*25}')


# 指定されたtarget IPアドレスとport番号にTCP接続を試みます。
# 接続が成功すれば、そのホストが利用可能であるとみなし、Trueを返します。
# 接続に失敗すると、例外がキャッチされ、エラーメッセージがログに記録された後にFalseを返します。
# 要は接続テスト
def is_found_host(target, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # 応答がなければ1秒後に接続ストップ
        sock.settimeout(1)
        try:
            sock.connect((target, port))
            return True
        except Exception as ex:
            logger.error({
                'action': 'is_found_host',
                'target': target,
                'port': port,
                'ex': ex
            })
            return False


# この関数は、ネットワーク上の近隣ホストを見つけるためのものです。
# 指定されたIP範囲(start_ip_rangeからend_ip_rangeまで)とポート範囲(start_portからend_portまで)を使用して、利用可能なホストを探索します。
def find_neighbours(my_host, my_port, start_ip_range, end_ip_range, start_port, end_port):

    address = f'{my_host}:{my_port}'
    m = RE_IP.search(my_host)
    if not m:
        return None


    """
    ex):
    prefix_host: 192.168.1.
    last_ip: 10
    """
    prefix_host = m.group('prefix_host')
    last_ip = m.group('last_ip')

    neighbours = []
    for guess_port in range(start_port, end_port):
        for ip_range in range(start_ip_range, end_ip_range):
            guess_host = f'{prefix_host}{int(last_ip)+int(ip_range)}'
            guess_address = f'{guess_host}:{guess_port}'
            #接続テスト
            if (is_found_host(guess_host, guess_port) and
                    not guess_address == address):
                neighbours.append(guess_address)
    return neighbours

# 現在のホストのIPアドレスを取得するためのもの
def get_host():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception as ex:
        logger.debug({'action': 'get_host', 'ex': ex})
    return '127.0.0.1'
