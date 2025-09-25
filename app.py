import base64
import json
import folium
from folium import IFrame, ClickForMarker
from folium.plugins import FloatImage, Geocoder
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

    geolocator = Nominatim(timeout=10, user_agent="Dinamitrii")


    maps_to = folium.Map(location=[json_data['lat'], json_data['lon']], zoom_start=12, tiles='OpenStreetMap',zoom_control="bottomleft")

    maps_to.add_child(Geocoder(), name='Geocoder').get_bounds()

    # folium.GeoJson(location=[json_data['lat'], json_data['lon']], name='walk_to').add_to(maps_to)

    tooltip = "Click to see @"
    html = '<img src="data:image/png;base64,{}">'.format
    picture1 = base64.b64encode(open('static/images/xtras/1.png', 'rb').read()).decode()
    iframe1 = IFrame(html(picture1), '300','300')
    popup1 = folium.Popup(iframe1, max_width=300)
    icon1 = folium.Icon(color111111111111111111111111111111111111111111111111111="blue", icon="info-sign")

    folium.Marker(location=[json_data['lat'], json_data['lon']], popup=popup1, tooltip=tooltip, icon=icon1).add_to(maps_to)

    url = (
        "https://raw.githubusercontent.com/ocefpaf/secoora_assets_map/"
        "a250729bbcf2ddd12f46912d36c33f7539131bec/secoora_icons/rose.png"
    )

    FloatImage(url, bottom=60, left=30).add_to(maps_to)




    maps_to.add_child(ClickForMarker())



    context = {

        'data': json_data,
        'map': maps_to,

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
