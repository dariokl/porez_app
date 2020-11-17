$(document).ready(function () {
    $(function () {
        $('#fields-0-name').val('').attr('read_label', 'JMBG - Korisnika')
        $('#fields-0-name').css('background', 'lightgray').attr('placeholder', $('#userVal').text())
        $('#fields-1-name').attr('read_label', 'Porezna godina').prop('required', true)
        $('#fields-2-name').hide()
        $('#fields-3-name').attr('read_label', 'Porezni period - OD').prop('required', true)
        $('#fields-4-name').attr('read_label', 'Porezni period - DO').prop('required', true)
        $('#fields-5-name').attr('read_label', 'Prihod ostvaren  iznajmljivanjem nepokretne imovine (BAM)')
        $('#fields-6-name').attr('read_label', 'Prihod ostvaren  iznajmljivanjem pokretne imovine (BAM)')
        $('#fields-7-name').attr('read_label', 'Troškovi odžavanja (BAM)')
        $('#fields-8-name').attr('read_label', 'Troškovi oglašavanja (BAM)')
        $('#fields-9-name').attr('read_label', 'Troškovi osiguranja (BAM)')
        $('#fields-10-name').attr('read_label', 'Takse i naknade za license (BAM)')
        $('#fields-11-name').attr('read_label', 'Troškovi nenaplativih potraživanja (BAM)')
        $('#fields-12-name').attr('read_label', 'Trošak amortizacije (BAM)')
        $('#fields-13-name').attr('read_label', 'Putni troškovi (BAM)')
        $('#fields-14-name').attr('read_label', 'Troškovi rezija koje plaća vlasnik (BAM)')
        $('#fields-15-name').attr('read_label', 'Kamate i bankovne naknade (BAM)')
        $('#fields-16-name').attr('read_label', 'Drugi troskovi u vezi s iznajmljivanjem (BAM)')
        $('#fields-17-name').attr('read_label', 'Ukupni troskovi').css('background', 'lightgray')
        $('#fields-18-name').attr('read_label', 'Troskovi koji se priznaju po procentu').css('background', 'lightgray')
        $('#fields-19-name').attr('read_label', 'Prihod od iznajmljivanja po odbitku troskova ').css('background', 'lightgray')
        $('#fields-20-name').attr('read_label', 'Ukupan iznos porza na iznajmljivanje imovine koji je tokom poreskog perioda uplacen kao akontacija (BAM) ')
        $('#fields-21-name').attr('read_label', 'Mjesecni iznos akontacije').css('background', 'lightgray')
        $('#fields-22-name').attr('read_label', 'Datum')
        $('#fields-23-name').attr('read_label', 'Ime i Prezime').val($('#userNVal').text()).prop('disabled', true)
        $('#fields-24-name').attr('read_label', 'Adresa')
        $('#fields-24-name').val($('#userAVal').text()).prop('disabled', true)
    });
    var l = []

    $(function () {
        $('input[type=text]').each(function (k, v) {
            if ($(v).attr('id') == 'address') {
            }
            else {
                l.push($(v).attr('read_label'))
            }
        })
    });

    $(function () {
        $('.fake_').each(function (k, v) {
            $(this).attr('class', 'fake_' + k);
            $(this).append(l[k])
        });
    });

    $('#fields-1-name').yearpicker({
        startYear: 2000,
        endYear: 2021,

    });

    $(function () {
        $('#fields-5-name').attr('type', 'number');
        $('#fields-6-name').attr('type', 'number');
        $('#fields-7-name').attr('type', 'number');
        $('#fields-8-name').attr('type', 'number');
        $('#fields-9-name').attr('type', 'number');
        $('#fields-10-name').attr('type', 'number');
        $('#fields-11-name').attr('type', 'number');
        $('#fields-12-name').attr('type', 'number');
        $('#fields-13-name').attr('type', 'number');
        $('#fields-14-name').attr('type', 'number');
        $('#fields-15-name').attr('type', 'number');
        $('#fields-16-name').attr('type', 'number');
        $('#fields-20-name').attr('type', 'number');

    });



    $("#fields-3-name").datepicker({
        format: "mm",
        viewMode: "months",
        minViewMode: "months",
    }).on('changeDate', function (e) {
        var minDate = new Date(e.date.valueOf());
        $('#fields-4-name').datepicker('setStartDate', minDate);
    });

    $("#fields-4-name").datepicker({
        format: "mm",
        viewMode: "months",
        minViewMode: "months",
    });

    $('#fields-22-name').datepicker({
        format: 'dd.mm.yy'
    })

    if ($('#fields-5-name').val().length === 0 && $('#fields-6-name').val().length === 0) {
        $('.next').fadeOut()
    }

    if ($('#fields-22-name').val().length != 0) {
        $('#fields-22-name').prop('disabled', true)
    }

});

$(function () {
    $("#msform :input").change(function () {
        var li = [$('#fields-7-name').val(), $('#fields-8-name').val(), $('#fields-9-name').val(), $('#fields-10-name').val(), $('#fields-11-name').val(), $('#fields-12-name').val(), $('#fields-13-name').val(), $('#fields-14-name').val(), $('#fields-15-name').val(), $('#fields-16-name').val()]
        var total = 0
        for (var i = 0; i < li.length; i++) {
            total += li[i] << 0;
        }
        $('#fields-17-name').val(total);
        var sum_7 = ((30 / 100) * $("#fields-6-name").val());
        var sum_7a = ((30 / 100) * $("#fields-5-name").val());
        $('#fields-18-name').val((sum_7 + sum_7a));
        var sum_18 =  $('#fields-18-name').val()
        $('#fields-19-name').val(parseInt(total) + parseInt(sum_18))
    });
});

$(function () {
    $('#fields-20-name').on('change keyup input', function () {
        var field = $('#fields-19-name').val();
        function multdec(val1, val2) {
            return (val1 * 10 + val2 * 10) / 100;
        }

        const diff = (a, b) => {
            return Math.abs(a - b);
        }
        shorten = (multdec(field, 0.1) / (diff($('#fields-4-name').val(), $('#fields-3-name').val()) +
            1)).toFixed(2)

        $('#fields-21-name').val(shorten);

    });
});




$("#msform :input, .datepicker, .select").on('change keyup input dateChange', function (e) {
    form = document.querySelector('#msform');
    if (form.reportValidity() == false) {
        if ($("div.error", $(this).parent()).length == 0) {
            var $div = $('<div class="col"></div>');
            $div.css({
                'background': '#FF5555',
                'color': 'black',
            })

            if ($(this).attr('type') == 'number') {
                $div.html('U polje je moguće unijeti samo broj !')
                $div.addClass('error'); //could also add the above styles to your css for .error and remove that code
            }

            //insert div after the input that changed
            $div.insertAfter($(this));
            $('.next').fadeOut()
        }
    }
    else {
        $('.next').fadeIn()
        $('.error').remove()
    }
});
