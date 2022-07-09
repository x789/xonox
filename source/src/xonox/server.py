# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

from collections import namedtuple
from flask import Flask, request, abort, jsonify, json, Response
from . import Config, Station, StationRepository, Preset, PresetRepository

# WebAPI Helpers #################
##################################
def convert_input_to(class_):
    '''A decorator to create an object from the JSON transferred in a request-body.'''
    def wrap(f):
        def decorator(*args):
            obj = class_(**request.get_json())
            return f(obj)
        return decorator
    return wrap

class ObjectToJsonStringEncoder(json.JSONEncoder):
    '''A JSON encoder that tries to serialize using 'to_json' or returns the dictionary of the object to serialize.'''
    def default(self, o):
        if hasattr(o, 'to_json'):
            return o.to_json()
        if isinstance(o, Station): # Change name of property 'stream' to 'streamUrl'
            o2 = dict(o.__dict__)
            o2['streamUrl'] = o2.pop('stream')
            return o2
        else:
            return o.__dict__

# WebAPI Initialization ##########
##################################
app = Flask(__name__)
stationRepository = None
presetRepository = None
stationTracker = dict() # used to track the last requested station per device to support presets/favorites
app.json_encoder = ObjectToJsonStringEncoder

# Management API #################
##################################
CreateStationDto = namedtuple('CreateStationDto', 'name description streamUrl')

@app.route('/station', methods=['post'])
@convert_input_to(CreateStationDto)
def create_station(dto):
    station = Station(dto.name, dto.description, dto.streamUrl)
    stationRepository.add(station)
    return Response(status=201, headers={'Location': '/station/' + str(station.id)}, content_type='application/json')

@app.route('/station', methods=['get'])
def get_station_list():
    return jsonify(stationRepository.get_all())

@app.route('/station/<int:id>', methods=['get'])
def get_station(id):
    try:
        return jsonify(stationRepository.get(id))
    except KeyError:
        return abort(404)

@app.route('/station/<int:id>', methods=['delete'])
def delete_station(id):
    try:
        stationRepository.remove(id)
        return Response(status=204)
    except KeyError:
        return abort(404)

# NOXON(tm) API ##################
##################################
@app.route('/setupapp/fs/asp/BrowseXML/loginXML.asp')
def get_root_menu():
    if (__get_device_id(request) is None):
        return '<EncryptedToken>a6703ded78821be5</EncryptedToken>'
    else:
        sorted_stations = sorted(stationRepository.get_all(), key=lambda x: x.name)
        return __create_station_list(sorted_stations, request.host_url)

@app.route('/setupapp/fs/asp/BrowseXML/Search.asp')
def search_station():
    requestedStationId = int(request.args.get('Search'))
    try:
        station = stationRepository.get(requestedStationId)
        __track_station(station, request)
        return __create_station_list([station], request.host_url)
    except IndexError:
        return abort(404)

@app.route('/Favorites/AddPreset.aspx')
def add_preset():
    device_id, preset_index = __get_device_and_preset_index(request)
    if device_id in stationTracker.keys():
        station_id = stationTracker[device_id]
        presetRepository.add(Preset(device_id, preset_index, station_id))
        result = '<?xml version="1.0" encoding="iso-8859-1" standalone="yes"?><ListOfItems><ItemCount>-1</ItemCount><Item><ItemType>Message</ItemType><Message>Preset set</Message></Item></ListOfItems>'
    else:
        result = '<?xml version="1.0" encoding="iso-8859-1" standalone="yes"?><ListOfItems><ItemCount>-1</ItemCount>'
        result = result + '<Item><ItemType>Message</ItemType><Message>Preset not created. Reselect the station to preset and then try again.</Message></Item>'
        result = result + '</ListOfItems>'
    return result

@app.route('/Favorites/GetPreset.aspx')
def get_preset():
    device_id, preset_index = __get_device_and_preset_index(request)
    try:
        preset = presetRepository.get(device_id, preset_index)
        station = stationRepository.get(preset.station_id)
        return __create_station_list([station], request.host_url)
    except KeyError:
        return '<?xml version="1.0" encoding="iso-8859-1" standalone="yes"?><ListOfItems><ItemCount>-1</ItemCount><Item><ItemType>Message</ItemType><Message>Preset not found</Message></Item></ListOfItems>'

@app.route('/noOp')
def no_op():
    return ''

def __create_station_list(stations, baseUri):
    result = '<?xml version="1.0" encoding="iso-8859-1" standalone="yes"?><ListOfItems><ItemCount>-1</ItemCount>'
    for station in stations:
        result = result + __station_to_xml(station, baseUri)
    result = result + '</ListOfItems>'
    return result

def __station_to_xml(station, baseUri):
    return '<Item><ItemType>Station</ItemType><StationId>' + str(station.id) + '</StationId><StationName>' + station.name + '</StationName><StationUrl>' + station.stream + '</StationUrl><StationDesc>' + station.description + '</StationDesc><StationFormat>Public</StationFormat><StationLocation>n/a</StationLocation><StationBandWidth>128</StationBandWidth><StationMime>MP3</StationMime><Relia>1</Relia><Bookmark>' + baseUri + '/noOp</Bookmark><Logo>' + baseUri + '/noOp</Logo></Item>'

def __track_station(station, request):    
    device_id = __get_device_id(request)
    stationTracker[device_id] = station.id

def __get_device_id(request):
    return str(request.args.get('mac'))

def __get_preset_index(request):
    return int(request.args.get('id'))

def __get_device_and_preset_index(request):
    return (__get_device_id(request), __get_preset_index(request))

# Application ####################
##################################
def run(host, config_directory):
    global stationRepository
    global presetRepository
    config = Config(config_directory)
    stationRepository = StationRepository(config)
    presetRepository = PresetRepository(config)
    app.run(host=host, port=80)