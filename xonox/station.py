# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

class Station:
    def __init__(self, name, description, stream, id = None):
        self.id = id
        self.name = name
        self.description = description
        self.stream = stream
