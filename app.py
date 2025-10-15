import os
import base64
import json
from pprint import pprint
import folium
from folium import IFrame, ClickForMarker
from folium.plugins import FloatImage, Geocoder, geocoder
from geopy.geocoders import Nominatim
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, url_for

load_dotenv(verbose=True)

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route('/')
@app.route('/index')
def index():
    ###
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)

    ###
    resp = requests.get('http://ip-api.com/json/', {'data': ip_data})
    text_data = resp.text
    json_data = json.loads(text_data)
    ###

    print(json_data)

    # weather_url=f"https://api.openweathermap.org/data/2.5/fwi?lat={json_data['lat']}&lon={json_data['lon']}&appid={os.getenv('API_KEY')}"
    #
    # weather_data = requests.get(weather_url).text
    #
    # weather_json = json.loads(weather_data)
    #
    #
    # pprint(weather_json)
    #
    #
    #
    #
    #
    geolocator = Nominatim(timeout=10, user_agent="Dinamitrii")

    loc = geolocator.geocode(json_data)

    geodata = loc.raw

    print(geodata)

    lat = loc.latitude
    lon = loc.longitude

    address = loc.address

    print(address)
    print(lat, lon)

    pprint(geodata)

    maps_to = folium.Map([lat, lon], tiles='OpenStreetMap', zoom_start=16, zoom_control="bottomleft")

    tooltip = "<a src='https://maps.google.com/'</a>"
    html = '<img src="data:image/png;base64,{}">'.format
    picture1 = base64.b64encode(open('static/images/xtras/1.png', 'rb').read()).decode()
    picture2 = base64.b64encode(open('static/images/xtras/12.png', 'rb').read()).decode()
    iframe1 = IFrame(html(picture1), '300', '300')
    iframe2 = IFrame(html(picture2), '300', '300')

    popup1 = (f"<a href='https://www.google.com/maps/embed/v1/view?key={os.getenv('API_KEY')}"
              f"&center={address}&zoom=18'>'</a>'")

    popup2 = folium.Popup(iframe2, max_width=300)
    icon1 = folium.Icon(color="blue", icon="info-sign")
    icon2 = folium.Icon(color="green", icon="info-sign")

    folium.Marker(location=(lat, lon), popup=popup1, tooltip=tooltip, icon=icon1).add_to(maps_to)

    Geocoder().add_to(maps_to)

    url = (
        "https://raw.githubusercontent.com/ocefpaf/secoora_assets_map/"
        "a250729bbcf2ddd12f46912d36c33f7539131bec/secoora_icons/rose.png"
    )

    FloatImage(url, bottom=60, left=30).add_to(maps_to)

    maps_to.add_child(ClickForMarker())

    context = {

        'data': json_data,
        'map': maps_to,
        'geodata': geodata,

    }

    maps_to.save('static/images/maps/maps_to.html')

    return render_template('index.html', **context)


@app.route("/favicon.ico")
def favicon():
    return (url_for('static', filename='images/favicon/favicon.ico'),
            url_for('static', filename='images/favicon/favicon-16x16.png'),
            url_for('static', filename='images/favicon/favicon-32x32.png'),
            url_for('static', filename='images/favicon/android-chrome-192x192.png'),
            url_for('static', filename='images/favicon/android-chrome-256x256.png'),
            url_for('static', filename='images/favicon/apple-touch-icon.png'),
            url_for('static', filename='images/favicon/safari-pinned-tab.svg'),
            url_for('static', filename='images/favicon/mstile-150x150.png'),
            url_for('static', filename='images/favicon/browserconfig.xml8lr'),
            url_for('static', filename='images/favicon/site.webmanifest'))


if __name__ == '__main__':
    app.run(port=8000)
