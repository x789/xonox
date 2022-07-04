# xonox - an alternative service for legacy NOXON(tm) devices
# (c) 2022 - TillW
# Licensed to you under Affero GPL 3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

from collections import namedtuple
from flask import Flask, request, abort, jsonify, json, Response
from . import Station, StationRepository, Preset, PresetRepository

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
    if (request.args.get('mac') is None):
        return '<EncryptedToken>a6703ded78821be5</EncryptedToken>'
    else:
        return __create_station_list(stationRepository.get_all(), request.host_url)

@app.route('/setupapp/fs/asp/BrowseXML/Search.asp')
def search_station():
    requestedStationId = int(request.args.get('Search'))
    try:
        station = stationRepository.get(requestedStationId)
        return __create_station_list([station], request.host_url)
    except IndexError:
        return abort(404)

@app.route('/Favorites/AddPreset.aspx')
def add_preset():
    result = '<?xml version="1.0" encoding="iso-8859-1" standalone="yes"?><ListOfItems><ItemCount>-1</ItemCount>'
    result = result + '<Item><ItemType>Message</ItemType><Message>not supported (yet)</Message></Item>'
    result = result + '</ListOfItems>'
    return result

@app.route('/Favorites/GetPreset.aspx')
def get_preset():
    device_id = str(request.args.get('mac'))
    preset_index = int(request.args.get('id'))
    preset = presetRepository.get(device_id, preset_index)
    station = stationRepository.get(preset.station_id)
    return __create_station_list([station], request.host_url)

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

# Application ####################
##################################
def run(host, configDirectory):
    global stationRepository
    global presetRepository
    stationRepository = StationRepository(configDirectory)
    presetRepository = PresetRepository(configDirectory)
    app.run(host=host, port=80)