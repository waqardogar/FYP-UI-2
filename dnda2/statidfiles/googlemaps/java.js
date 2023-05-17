function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    document.getElementById('open').style.display = 'none'
  }
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    document.getElementById('open').style.display = 'inline'
  }

// Show Map
mapboxgl.accessToken = 'pk.eyJ1Ijoid2FxYXJtdW4iLCJhIjoiY2xmNnB0MnZ3MHhjMjN5cWh3YWtnMHZsMyJ9.DdA5uGyoRwdIZp9u0hK-SA';
const map = new mapboxgl.Map({
container: 'map',
style: 'mapbox://styles/mapbox/satellite-streets-v12', 
center: [74.24076031193948, 31.39222922632956],
zoom: 17 // 
});
// End Show map

map.addControl(new mapboxgl.NavigationControl());
 draw = new MapboxDraw({
displayControlsDefault: false,
controls: {
polygon: true,
trash: true
},
});
map.addControl(draw);
map.on('draw.create', updateArea);
map.on('draw.delete', updateArea);
map.on('draw.update', updateArea);
map.addControl(
new mapboxgl.GeolocateControl({
positionOptions: {
enableHighAccuracy: true
},
trackUserLocation: true,
showUserHeading: true
})
);
 marker = new mapboxgl.Marker({
draggable: false
})
.setLngLat([74.24076031193948, 31.39222922632956])
.addTo(map);
// function onDragEnd() {
// const lngLat = marker.getLngLat();
// function cordin(lngLat){
//     return lngLat
// }
// var start = [lngLat.lng,lngLat.lat]
// }
// marker.on('dragend', onDragEnd);

function updateArea(e) {
const data = draw.getAll();
cor=data['features'][0]['geometry']['coordinates'][0];
console.log(cor)
if (data.features.length > 0) {
const area = turf.area(data);
const rounded_area = Math.round(area * 100) / 100;
} else {
answer.innerHTML = '';
if (e.type !== 'draw.delete')
alert('Click the map to draw a polygon.');
}
var overlap = document.getElementById("overlap").value
var aspect = document.getElementById("ar").value
var fa = document.getElementById("fa").value
var tt = document.getElementById("tt").value
var data2 = {'cordinates':cor,'overlapingrate':overlap,
'flightAltitude':fa,'aspectratio':aspect,"tree":tt

}
 var csrftoken = getCookie('csrftoken');
 $.ajax({
     type: 'POST',
     url: 'pp/',
     data: data2,
     headers: {'X-CSRFToken': csrftoken}, 
     success: function(data1) {
      var coveragePathFeature = turf.lineString(data1);
        // console.log(typeof(data1))
          // var zigzag = {
          //   "type": "Feature",
          //   "geometry": {
          //     "type": "LineString",
          //     "coordinates": coveragePathFeature
          //   },
          //   "properties": {}
          // };
          // map.on('idle', function() {
          //   map.addLayer({
          //     "id": "zigzag",
          //     "type": "line",
          //     "source": {
          //       "type": "geojson",
          //       "data": zigzag
          //     },
          //     "layout": {
          //       "line-join": "round",
          //       "line-cap": "round"
          //     },
          //     "paint": {
          //       "line-color": "#ff0000",
          //       "line-width": 3
          //     }
          //   });
          
          // });
          map.on('load', function() {
            map.addLayer({
                'id': 'coveragePath',
                'type': 'line',
                'source': {
                    'type': 'geojson',
                    'data': coveragePathFeature
                },
                'layout': {
                    'line-join': 'round',
                    'line-cap': 'round'
                },
                'paint': {
                    'line-color': '#007cbf',
                    'line-width': 3
                }
            });
        });
        
     },
     error: function(xhr, textStatus, errorThrown) {
         console.log('Error sending data: ' + errorThrown);
     }
 });
 function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie !== '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = cookies[i].trim();
             if (cookie.substring(0, name.length + 1) === (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
 }
}


