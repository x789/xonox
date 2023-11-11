# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

from argparse import ArgumentParser
from xonox import server

if __name__ == "__main__":
    parser = ArgumentParser(description = 'An alternative infrastructure-service for legacy Noxon(tm) devices.')
    parser.add_argument('--host', default='0.0.0.0', required=False, help='IP address to bind to. If omitted, xonox bind to all available interfaces.')
    parser.add_argument('--config-dir', default=None, dest='config_dir', help='Directory that contains the configuration. If omitted, the user\'s home directory is used.')
    
    args = parser.parse_args()
    server.run(args.host, args.config_dir)