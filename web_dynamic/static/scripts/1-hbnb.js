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
});