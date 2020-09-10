function make_subform(val) {
    var tag = 'subform_' + val;
    var el = ('<div class="subform" style="display: flex; flex-direction: column;">' +
        '<input id="' + tag + '_fname" type="text" placeholder="Name"></input>' +
        '<input id="' + tag + '_lname" type="text" placeholder="Jedinica"></input>' +
        '<input id="' + tag + '_add1" type="text" placeholder = "KM"></input>' +
        '<input id="' + tag + '_add2" type="text" placeholder = "Ukupna"></input>' +
        '</div>');
    var $el = $(el);
    $el.data('value', val);
    return $el;
}

$(function() {
    $('.row').on('change', 'select', function(e) {
        var value = $(e.target).val();
        $(".sub_forms").append(make_subform(value));
        $(this).find('[value='+value+']').remove();
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
                console.log('done')
            }
        });
        event.preventDefault();
   });
});