$(function () {
    $('#searchBtn').on('click', function (e) {
        $('#add_to').empty();
        $.ajax({
            url: '/livesearch',
            method: 'POST',
            data: JSON.stringify({'name': $("#table_filter").val(), 'date':$("input[name='radios']:checked").val() }),
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                dataChart(data);
            }
        })
        e.preventDefault();
    });
});

function make_subform(val, name, id) {
    var tag = 'subform_' + val;
    var url = '';
    var img = '';
    if (name === 'PRIM-1054') {
        url = '/render_1054/';
        img = '/static/img/prvi-page-001.jpg';
    } else {
        url = '/render_razrez/';
        img = '/static/img/drugi-page-001.jpg';
    }
    var el = ('<div class="col-md-6 col-lg-4 pb-3" data-aos="fade-up" data-aos-duration="1000">\n' + '                  <div class="card card-custom bg-white border-white border-0">\n' +
        '          <div class="card-custom-img" style="background-image: url('+img+'); background-size: contain;"></div>\n' +
        '          <div class="card-custom-avatar">\n' +
        '            <img class="img-fluid" src="/static/img/ProfileLogo.png" alt="Avatar" />\n' +
        '          </div>\n' +
        '          <div class="card-body" style="overflow-y: auto">\n' +
        '            <h4 class="card-title">' + name + '</h4>\n' +
        '            <p class="card-text">Card has minimum height set but will expand if more space is needed for card body content. You can use Bootstrap <a href="https://getbootstrap.com/docs/4.0/components/card/#card-decks" target="_blank">card-decks</a> to align multiple cards nicely in a row.</p>\n' +
        '          </div>\n' +
        '          <div class="card-footer" style="background: inherit; border-color: inherit;">\n' +
        '            <a href="' + url + '' + id + '" class="btn btn-primary">Download</a>\n' +
        '            <a href="#" class="btn btn-outline-primary">Other option</a>\n' +
        '          </div>\n' +
        '                    ' +
        '\n' +
        '        </div></div>');
    var $el = $(el);
    $el.data('value', val);
    return $el;
};

function dataChart(value) {
    if (value.name){
    var i = 0;
    for (i = 0; i < value.name.length; i++) {
        $('#add_to').append(make_subform(i, value.name[i], value.id[i]));
    }}
    else {
        $('#add_to').append('<div class="container">' +
            '<h1 class="text-center">Provjerite ime obrasca !</h1>' +
            '</div>')
    }
};