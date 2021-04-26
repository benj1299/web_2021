mapboxgl.accessToken = 'pk.eyJ1IjoiYmVuajEyOTkiLCJhIjoiY2pvZGI2bDFiMmNzeDNxbzE4cm53aXc1NiJ9.eN1THAwDModYkQO9gFQ4SA';

var map = new mapboxgl.Map({
container: 'map',
style: 'mapbox://styles/mapbox/streets-v11',
center: [2.33202934968712, 48.85533393993753], // starting position
zoom: 12 // starting zoom
});

var geocoder = new MapboxGeocoder({
  accessToken: mapboxgl.accessToken,
  mapboxgl: mapboxgl,
  countries: "fr",
});
   
document.getElementById('geocoder').appendChild(geocoder.onAdd(map));

geocoder.on('results', function(results) {
  element = document.getElementById("hidden")
  lat = results.features[0].center[0]
  longitude = results.features[0].center[1]
  element.innerHTML = "<input type='hidden' name='lat' value='"+ lat +"' /><input type='hidden' name='longitude' value='"+ longitude +"' />"
  console.log(results);
})

$(document).ready(function() {
  $('.selector').select2();
});

function updateTextInput(val) {
  document.getElementById('result_range').innerHTML="Max: " + val +"€";
}