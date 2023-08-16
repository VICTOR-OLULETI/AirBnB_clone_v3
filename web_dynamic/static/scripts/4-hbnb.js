$(document).ready(function () {
    let amtyObj = {}
    $(".amenities .popover input").change(function () {
        if ($(this).is(':checked')) {
            amtyObj[$(this).attr('data-id')] = $(this).attr('data-name');
        }
        else {
            delete amtyObj[$(this).attr('data-id')]
        }
    let objs = Object.values(amtyObj);
    if (objs.length > 0) {
        $('div.amenities > h4').text(objs.join(', '));
    }
    else {
        $('div.amenities > h4').html('&nbsp;');
    }
    });
    $.ajax({
        url: "http://0.0.0.0:5001/api/v1/status/",
        method: 'GET',
        success: function(response) {
        if (response.status === 'OK'){
            $("#api_status").addClass("available");
        }
        else {
            $("#api_status").removeClass("available");
        }
        },
        error: function() {}
    });
    $.ajax({
        url: "http://0.0.0.0:5001/api/v1/places_search/",
        method: 'POST',
        data: '{}',
        contentType: 'application/json',
        success: function(response) {
            for (let i = 0; i < response.length; i++) {
                let place = response[i];
                $('.places').append('<article><div class="title"><h2>'
                    + place.name + '</h2><div class="price_by_night"><p>$'
                    + place.price_by_night + '</p></div></div><div class="information"><div class="max_guest"><div class="guest_image"></div><p>'
                    + place.max_guest
                    + '</p></div><div class="number_rooms"><div class="bed_image"></div><p>'
                    + place.number_rooms + '</p></div><div class="number_bathrooms"><div class="bath_image"></div><p>'
                    + place.number_bathrooms + '</p></div></div><div class="description"><p>'
                    + place.description + '</p></div></article>');
            }
        },
        error: function() {}
    });
    $('.filter > button').click(function () {
        $('.places > article').remove();
        $.ajax({
            url: "http://0.0.0.0:5001/api/v1/places_search/",
            method: 'POST',
            data: JSON.stringify({'amenities': Object.keys(amtyObj)}),
            contentType: 'application/json',
            success: function(response) {
                for (let i = 0; i < response.length; i++) {
                    let place = response[i];
                    $('.places').append('<article><div class="title"><h2>'
                        + place.name + '</h2><div class="price_by_night"><p>$'
                        + place.price_by_night + '</p></div></div><div class="information"><div class="max_guest"><div class="guest_image"></div><p>'
                        + place.max_guest
                        + '</p></div><div class="number_rooms"><div class="bed_image"></div><p>'
                        + place.number_rooms + '</p></div><div class="number_bathrooms"><div class="bath_image"></div><p>'
                        + place.number_bathrooms + '</p></div></div><div class="description"><p>'
                        + place.description + '</p></div></article>');
                }
            },
            error: function() {}
        })
    })
});