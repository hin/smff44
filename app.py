from flask import Flask, render_template
import xml.etree.ElementTree as ET
import pprint

ns = {'kml': 'http://www.opengis.net/kml/2.2'}

app = Flask('smff44')

areas = []

@app.route('/')
def index():
    return render_template('map.html', areas=areas)

def get_id(e):
    s = e.findall('./kml:name', ns)[0].text
    return s.split(',')[0]
    
def get_name(e):
    s = e.findall('./kml:name', ns)[0].text
    s = s.split(',')[1]
    return s

def get_position(e):
    s = e.findall('./kml:Point/kml:coordinates', ns)[0].text
    v = s.split(',')
    return float(v[1]), float(v[0])
    
def get_locator(e):
    s = e.findall('./kml:description', ns)[0].text
    return s[0:6]
    
def get_description(e):
    s = e.findall('./kml:description', ns)[0].text
    return s[11:]
    
def parse_kml():
    tree = ET.parse('smff.kml')
    root = tree.getroot()
    areas = []
    for e in root.findall('./kml:Folder/kml:Placemark', ns):
        if e.findall('./kml:styleUrl', ns)[0].text in ['#smffred', '#smffyellow', '#smffgreen']:
            area = {
                'id': get_id(e),
                'name': get_name(e),
                'descr': get_description(e),
                'locator': get_locator(e),
                'position': get_position(e),
                }
            areas.append(area)
    return areas

if __name__ == '__main__':
    areas = parse_kml()
#    pp = pprint.PrettyPrinter(indent=4)
#    print pp.pprint(areas)
    app.run(debug=True)
