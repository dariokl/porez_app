$(document).ready(function() {
    $('.next').fadeOut()
    $('#select option[value="0"').prop('disabled select', true)
})


function make_subform(val, title) {
    var tag = 'subform_' + val;
    var el = ('<div class="subform" style="display: flex; flex-direction: column;">' +
        '<h4>' + title + '</h4>' +
        '<span> Adresa i Broj </span>' +
        '<input id="' + tag + '_fname" type="text" placeholder="Lokacija imovine"></input>' +
        '<span > Jedinica Mjere </span>'+
        '<input id="' + tag + '_lname" type="text" placeholder="Jedinica Mjere"></input>' +
        '<span> Broj/Jedinica Mjere </span>'+
        '<input id="' + tag + '_add1" type="text" placeholder="Broj Jedinica Mjere"></input>' +
        '<span> Iznos Poreza</span>'+
        '<input id="' + tag + '_add2" type="text" placeholder="Porez po Jedinici Mjere"></input>' +
        '<span> Ukupno </span>'+
        '<input id="' + tag + '_add3" type="text" placeholder="Iznos Poreza"></input>' +
        '</div>');
    var $el = $(el);
    $el.data('value', val);
    return $el;
}

String.prototype.insert = function (index, string) {
  var ind = index < 0 ? this.length + index  :  index;
  return  this.substring(0, ind) + string + this.substr(ind);
};

function check_id(id){
    var counter = 0;
    $('.sub_forms').children().each(function(index, value){
        var data_dict= {}
        var $el = $(value);
        var key = $el.data('value');
        var val = []
        $el.find('input').each(function(_,v){val.push(v.value);});
        data_dict[key] = val;
        if (data_dict[id]) {
            counter = 1
        }
        else if (data_dict[id.insert(-1, '2')])
        {
            counter = 2
        }

    })
    return counter


}

$(function() {
    $('.row').on('change', 'select', function(e) {
        var value = $(e.target).val();
        var title = $(this).find('option:selected').text()
        if (check_id(value) === 0) {
            $('.sub_forms').append(make_subform(value, title));
            $(this).find('[value="+value+"]').remove();
        }
        else if (check_id(value) === 1){
            $('.sub_forms').append(make_subform(value.insert(-1, '2'), title));
            $(this).find('[value="+value+"]').remove();
        }
        else {
           var $div = $('<div class="mt-2 col"></div>');
           $div.css({
               'background': '#FF5555',
               'color': 'black',
           })
           if ($("div.error", $(this).parent()).length == 0) {
            $div.html('Maksimalan broj za kategoriju nekretnine !' )
            $div.addClass('error'); //could also add the above styles to your css for .error and remove that code
            $div.insertAfter($(this));

           }
        }
        $(e.target).val(0);
        $('.next').fadeIn();
        

    });
});

$(function() {
   $("#ajax_post").click(function (event) {
      var data_dict = {}
      $('.sub_forms').children().each(function (index, value) {
         var $el = $(value);
         var key = $el.data('value');
         var val = [];
         $el.find('input').each(function(_,v){val.push(v.value);});
         data_dict[key] = val;
      });
        $.ajax({
            type: 'POST',
            url: "/step_1",
            data: JSON.stringify(data_dict) ,
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
            }
        });
        event.preventDefault();
   });
});