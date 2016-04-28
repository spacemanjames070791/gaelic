/**
 * Created by Neil on 26/04/2016.
 */

var geocoder;
var map;
var marker;

$(document).ready(function () {

    google.maps.event.addDomListener(window, 'load', initialize);
    if(!!navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(handlePosition);
        doLocation();
    }
});

function doLocation(loc) {
    $.ajax({
        type: "GET",
        url: URL + "location/" + loc,
        async: true,
        contentType: "application/javascript",
        dataType: 'jsonp',
        success: function (json) {
            updateLoc(json);
        },
        error: function (e) {
            popupConfirm("Error", e.message);
            alert("failure");
        }
    });
}

function updateLoc(json){
    for (index = 0; index < json.length; index++) {
        $("#postcode").text(json[0].townName + ' - ' + json[0].gaelic);
    }
}

function initialize() {
    geocoder = new google.maps.Geocoder();
}

function handlePosition(positionData) {
    codeLatLng(positionData.coords);
}

function doGeoCode(latlng) {
    geocoder.geocode({'latLng': latlng}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            if (results[1]) {

                marker = new google.maps.Marker({
                    position: latlng,
                    map: map
                });
                var location = results[0].address_components[2].long_name;
                doLocation(location);
                $("#postcode").text(location);

            } else {
                alert('No results found');
            }
        } else {
            alert('Geocoder failed due to: ' + status);
        }
    });
}

function codeLatLng(coords) {
    var latlngStr = coords.latitude + ',' + coords.longitude,
        lat = coords.latitude,
        lng = coords.longitude,
        latlng = new google.maps.LatLng(lat, lng),

        mapOptions = {
            zoom: 11,
            center: latlng,
            mapTypeId: 'roadmap'
        };
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    doGeoCode(latlng);
}
