$(document).ready(function () {
    $('#fields-0-name').prop('disabled', true)
    $('#fields-18-name').prop('disabled', true)
    $('#fields-23-name').prop('disabled', true)
    $("#msform input[type=text]:not(#fields-0-name):not(#fields-23-name)").each(function () {
        $(this).val("")
    });
    $('#fields-1-name').attr('placeholder', 'Porezna godina')
    $('#fields-2-name').attr('placeholder', 'Sifra općine')
    $('#fields-3-name').attr('placeholder', 'Porezni period - OD')
    $('#fields-4-name').attr('placeholder', 'Porezni period - DO')
    $('#fields-5-name').attr('placeholder', 'Prihod ostvaren  iznajmljivanjem nepokretne imovine')
    $('#fields-6-name').attr('placeholder', 'Prihod ostvaren  iznajmljivanjem pokretne imovine')
    $('#fields-7-name').attr('placeholder', 'Troškovi odžavanja')
    $('#fields-8-name').attr('placeholder', 'Troškovi oglašavanja')
    $('#fields-9-name').attr('placeholder', 'Troškovi osiguranja')
    $('#fields-10-name').attr('placeholder', 'Takse i naknade za license')
    $('#fields-11-name').attr('placeholder', 'Troškovi nenaplativih potraživanja')
    $('#fields-12-name').attr('placeholder', 'Trošak amortizacije')
    $('#fields-13-name').attr('placeholder', 'Putni troškovi')
    $('#fields-14-name').attr('placeholder', 'Troškovi rezija koje plaća vlasnik')
    $('#fields-15-name').attr('placeholder', 'Kamate i bankovne naknade')
    $('#fields-16-name').attr('placeholder', 'Kamata i bankovne naknade')
    $('#fields-17-name').attr('placeholder', 'Drugi troskovi u vezi s iznajmljivanjem')
    $('#fields-18-name').attr('placeholder', 'Ukupni troskovi')
    $('#fields-24-name').attr('placeholder', 'Adresa')

});

    $("#fields-17-name").change(function(){
        var li = [$('#fields-5-name').val(), $('#fields-6-name').val(), $('#fields-7-name').val(), $('#fields-8-name').val(), $('#fields-9-name').val(), $('#fields-10-name').val(), $('#fields-11-name').val(), $('#fields-12-name').val(), $('#fields-13-name').val(), $('#fields-14-name').val(), $('#fields-15-name').val(), $('#fields-16-name').val()]
        var total = 0
        for (var i = 0; i < li.length; i++) {
            total += li[i] << 0;
        }
        $('#fields-18-name').val(total)


    })