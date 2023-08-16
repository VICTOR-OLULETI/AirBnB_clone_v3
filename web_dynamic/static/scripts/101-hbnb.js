$(document).ready(function () {
    let amtyObj = {};
    $(".amenities .popover input").change(function () {
        if ($(this).is(':checked')) {
            amtyObj[$(this).attr('data-id')] = $(this).attr('data-name');
        }
        else {
            delete amtyObj[$(this).attr('data-id')];
        }
        let objs = Object.values(amtyObj);
        if (objs.length > 0) {
            $('div.amenities > h4').text(objs.join(', '));
        }
        else {
            $('div.amenities > h4').html('&nbsp;');
        }
    });

    let stateObj = {};
    $(".locations > .popover > input").change(function () {
        if ($(this).is(':checked')) {
            stateObj[$(this).attr('data-id')] = $(this).attr('data-name');
        } else {
            delete stateObj[$(this).attr('data-id')]
        }
        let objs2 = Object.values(stateObj);
        if (objs2.length > 0) {
            $('div.locations > h4').text(objs2.join(', '));
        } else {
            $('div.locations > h4').html('&nbsp;');
        }
    });
    let cityObj = {}
    $(".locations > .popover > li > ul > li > input ").change(function () {
        if ($(this).is(':checked')) {
            cityObj[$(this).attr('data-id')] = $(this).attr('data-name');
        } else {
            delete cityObj[$(this).attr('data-id')];
        }
        let objs3 = Object.values(cityObj);
        if (objs3.length > 0) {
            $('div.locations > h4').text(objs3.join(', '));
        } else {
            $('div.locations > h4').html('&nbsp;');
        }
    });
    let reviews = []
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
                    + place.description + '</p></div>'+
                    '<div class="review"><h2>Reviews</h2><span>Show</span>' + 
                    '<ul id="{{ place.id }}"></ul></div></article>');
                reviews.push(place.reviews.join(', '))
            }
        },
        error: function() {}
    });

    $('.filter > button').click(function () {
        $('.places > article').remove();
        $.ajax({
            url: "http://0.0.0.0:5001/api/v1/places_search/",
            method: 'POST',
            data: JSON.stringify({'amenities': Object.keys(amtyObj), 'states': Object.keys(stateObj), 'cities': Object.keys(cityObj)}),
            contentType: 'application/json',
            success: function(response) {
                for (let i = 0; i < response.length; i++) {
                    let place = response[i];
                    reviews.push(place.reviews.join(', '));
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
    $('.review > span').click(function(reviews) {
        if ($('.review > span').text() == 'Show')
        {
            $('.review > span').text('Hide');
            if (reviews.length != 0) {
                for (let i = 0; i < reviews.length; i++) {
                    let r = reviews[i];
                    $('.review > ul').append('<li>' + r + '</li>')
                }
            }
        } else {
            $('.review > ul').empty();
            $('.review > span').text('Show');
        }
    });
});

});