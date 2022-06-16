# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

from xonox import server
import sys

if __name__ == "__main__":
    host = '0.0.0.0'
    if len(sys.argv) == 2:
        host = sys.argv[1]
    server.run(host)