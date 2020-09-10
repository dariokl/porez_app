$(function () {
    console.log('a')
    $(".row").on('change', 'select', function() {
        var list = ['<input type="text" placeholder="Adresa" name="string_" required>', '<input type="text" placeholder="Jedinica mjere" requred>']
        list.forEach(function (value, index) {
            $('#add_to').append(value)
        });
        $(this).clone().appendTo("#add_to")
        $("select").each(function (index, value) {
            $(this).attr('name', 'select_' + index)
            $('option').attr('name', 'option_' + index)
        })
        $("input[type=text]").each(function(index, value){
            $(this).attr("name", "string_" + index)
        })
        var ovo = $('#add_to')
        ovo.find('input:text, select').each(function(index, value){

        })
    });
});

$(function () {
    $("#ajax_post").click(function (event) {
        var data_dict = {}
        $('#add_to').find("input:text , select").each(function(index, value){

                data_dict['['+$(value).attr('name')+'].Value'] = $(this).val()


        })
        $.ajax({
            type: 'POST',
            url: "/prijava_razrez_im",
            data: data_dict ,
            success: function (data) {
                console.log('done')
            }
        });
        event.preventDefault();
    })
})