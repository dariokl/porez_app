$(document).ready(function () {
    $(function () {
        $("#msform input[type=text]:not(#fields-0-name):not(#fields-23-name)").each(function () {
            $(this).val("")
        });

        $('#fields-0-name').css('background', 'lightgray')
        $('#fields-1-name').attr('placeholder', 'Porezna godina').prop('required', true)
        $('#fields-2-name').hide()
        $('#fields-3-name').attr('placeholder', 'Porezni period - OD').prop('required', true)
        $('#fields-4-name').attr('placeholder', 'Porezni period - DO').prop('required', true)
        $('#fields-5-name').attr('placeholder', 'Prihod ostvaren  iznajmljivanjem nepokretne imovine (BAM)')
        $('#fields-6-name').attr('placeholder', 'Prihod ostvaren  iznajmljivanjem pokretne imovine (BAM)')
        $('#fields-7-name').attr('placeholder', 'Troškovi odžavanja (BAM)')
        $('#fields-8-name').attr('placeholder', 'Troškovi oglašavanja (BAM)')
        $('#fields-9-name').attr('placeholder', 'Troškovi osiguranja (BAM)')
        $('#fields-10-name').attr('placeholder', 'Takse i naknade za license (BAM)')
        $('#fields-11-name').attr('placeholder', 'Troškovi nenaplativih potraživanja (BAM)')
        $('#fields-12-name').attr('placeholder', 'Trošak amortizacije (BAM)')
        $('#fields-13-name').attr('placeholder', 'Putni troškovi (BAM)')
        $('#fields-14-name').attr('placeholder', 'Troškovi rezija koje plaća vlasnik (BAM)')
        $('#fields-15-name').attr('placeholder', 'Kamate i bankovne naknade (BAM)')
        $('#fields-16-name').attr('placeholder', 'Drugi troskovi u vezi s iznajmljivanjem (BAM)')
        $('#fields-17-name').attr('placeholder', 'Ukupni troskovi').css('background', 'lightgray')
        $('#fields-18-name').attr('placeholder', 'Troskovi koji se priznaju po procentu').css('background', 'lightgray')
        $('#fields-19-name').attr('placeholder', 'Prihod od iznajmljivanja po odbitku troskova ').css('background', 'lightgray')
        $('#fields-20-name').attr('placeholder', 'Ukupan iznos porza na iznajmljivanje imovine koji je tokom poreskog perioda uplacen kao akontacija (BAM) ')
        $('#fields-21-name').attr('placeholder', 'Mjesecni iznos akontacije').css('background', 'lightgray')
        $('#fields-22-name').attr('placeholder', 'Datum')
        $('#fields-23-name').attr('placeholder', 'Ime i Prezime')
        $('#fields-24-name').attr('placeholder', 'Adresa')
    });
    var l = []

    $(function () {
        $('input[type=text').each(function (k, v) {
            l.push(v['placeholder'])
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
    $('.next').fadeOut()


});

$(function () {
    $("#msform :input").change(function () {
        var li = [$('#fields-7-name').val(), $('#fields-8-name').val(), $('#fields-9-name').val(), $('#fields-10-name').val(), $('#fields-11-name').val(), $('#fields-12-name').val(), $('#fields-13-name').val(), $('#fields-14-name').val(), $('#fields-15-name').val(), $('#fields-16-name').val()]
        var total = 0
        for (var i = 0; i < li.length; i++) {
            total += li[i] << 0;
        }
        $('#fields-17-name').val(total)
        if ($("#fields-5-name").val() === '') {
            var sum = ((30 / 100) * $("#fields-6-name").val())
            $("#fields-18-name").val(sum)
            $("#fields-19-name").val($("#fields-6-name").val() - $('#fields-18-name').val())
        } else {
            var sum = ((30 / 100) * $("#fields-5-name").val())
            $("#fields-18-name").val(sum)
            $("#fields-19-name").val($("#fields-5-name").val() - $('#fields-18-name').val())
        }
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
