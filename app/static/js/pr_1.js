$(function () {
    console.log('a')
    $(".row").on('change', 'select', function() {
        var list = ['<input type="text" placeholder="Adresa" name="string_" required>', '<input type="text" placeholder="Jedinica mjere" requred>']
        list.forEach(function (value, index) {
            console.log(value)
            $('#add_to').append(value)

        });
        $(this).clone().appendTo("#add_to")
        $("select").each(function (index, value) {
            $(this).attr('id', 'select_' + index)
        })
        $("input[type=text]").each(function(index, value){
            $(this).attr("name", "string_" + index)
        })
    });
});

$(function () {
    $("#ajax_post").click(function (event) {
        var data_dict = {}
        $("input[type=text]").each(function(index){
                data_dict['['+$(this).attr('name')+'].Key'] = $(this).attr('name');
                data_dict['['+$(this).attr('name')+'].Value'] = $(this).val();
        });
        console.log(data_dict)
        $.ajax({
            type: 'POST',
            url: "/prijava_razrez_im",
            data: data_dict ,
            success: function (data) {
                console.log(data_dict)
            }
        });
        event.preventDefault();
    })
})