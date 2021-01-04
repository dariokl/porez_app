$(document).ready(function () {
    $(function () {
        $('#fields-0-name').val('').attr('read_label', 'JMBG - Korisnika')
        $('#fields-0-name').css('background', 'lightgray').attr('placeholder', $('#userVal').text())
        $('#fields-1-name').attr('read_label', 'Porezna godina').prop('required', true)
        $('#fields-2-name').hide()
        $('#fields-3-name').attr({'read_label': 'Porezni period - OD', 'has_tool': 'true', 'tool_value': 'Upisati OD kojeg mjeseca u gore navedenoj poreznoj godini se odnosi prijava poreza'}).prop('required', true)
        $('#fields-4-name').attr({'read_label' : 'Porezni period - DO', 'has_tool': 'true', 'tool_value': 'Upisati DO kojeg mjeseca u gore navedenoj poreznoj godini se odnosi prijava poreza' }).prop('required', true)
        $('#fields-5-name').attr({'read_label': 'Prihod ostvaren  iznajmljivanjem nepokretne imovine (BAM)', 'has_tool' : 'true', 'tool_value':'Koliko novca ste ukupno dobili ili vam je uplačeno u navedenoj godini od iznajmljivanja nepokretne imovine (stan, kuća, garaža i sl)' })
        $('#fields-6-name').attr({'read_label': 'Prihod ostvaren  iznajmljivanjem pokretne imovine (BAM)', 'has_tool' : 'true', 'tool_value' :'Koliko novca ste ukupno dobili ili vam je uplačeno u navedenoj godini od iznajmljivanja vaše pokretne imovine (vozilo, motocikl, čamac i sl)'})
        $('#fields-7-name').attr({'read_label' : 'Troškovi odžavanja (BAM)', 'has_tool': 'true', 'tool_value': 'Ukupan iznos dokumentovanih troškovai godišnjeg oodržavanja imovine koja se iznajmljivala nastali tokom poreznog perioda'})
        $('#fields-8-name').attr({'read_label': 'Troškovi oglašavanja (BAM)', 'has_tool': 'true', 'tool_value': 'Unesite dokumentovani iznos troškova ako ste plačali u oglašavanje za iznajmljivanje vaše imovine u navedenom poreznom periodu'})
        $('#fields-9-name').attr({'read_label': 'Troškovi osiguranja (BAM)', 'has_tool': 'true', 'tool_value': 'Unesite dokumentovani iznos troškova osiguranja iznajmljivane imovine u navedenom poreznom periodu'})
        $('#fields-10-name').attr({'read_label': 'Takse i naknade za license (BAM)', 'has_tool': 'true', 'tool_value': 'Iznos uplačen za takse i naknade za licence a vezane za iznajmljenu imovinu u navedenom poreznom periodu'})
        $('#fields-11-name').attr('read_label', 'Troškovi nenaplativih potraživanja (BAM)')
        $('#fields-12-name').attr({'read_label': 'Trošak amortizacije (BAM)', 'has_tool': 'true', 'tool_value':'Iznos amortizacije vezane za iznajmljenu imovinu u navedenom poreznom periodu'})
        $('#fields-13-name').attr({'read_label': 'Putni troškovi (BAM)', 'has_tool': 'true', 'tool_value' : 'Iznos putnih troškova vezanih za iznajmljenu imovinu u navedenom poreznom periodu'})
        $('#fields-14-name').attr({'read_label': 'Troškovi rezija koje plaća vlasnik (BAM)', 'has_tool': 'true', 'tool_value': 'Iznos režijskih troškova vezanih za iznajmljenu imovinu u navedenom poreznom periodu' })
        $('#fields-15-name').attr({'read_label': 'Kamate i bankovne naknade (BAM)', 'has_tool': 'true', 'tool_value': 'Iznos kamata i bankovnih naknada vezanih za iznajmljenu imovinu u navedenom poreznom periodu'})
        $('#fields-16-name').attr({'read_label': 'Drugi troskovi u vezi s iznajmljivanjem (BAM)', 'has_value': 'true', 'tool_value' : 'Ostali ne navedeni troškovi'})
        $('#fields-17-name').attr({'read_label': 'Ukupni troskovi', 'has_tool': 'true', 'tool_value':'Zbir svih navedenih troškova'}).css('background', 'lightgray')
        $('#fields-18-name').attr({'read_label': 'Troskovi koji se priznaju po procentu', 'has_tool': 'true', 'tool_value' : 'Troškovi koji su 30% od navedenih prihoda'}).css('background', 'lightgray')
        $('#fields-19-name').attr({'read_label': 'Prihod od iznajmljivanja po odbitku troskova ', 'has_tool': 'true', 'tool_value' : 'Prihodi umanjeni za 30%'}).css('background', 'lightgray')
        $('#fields-20-name').attr({'read_label': 'Ukupan iznos porza na iznajmljivanje imovine koji je tokom poreskog perioda uplacen kao akontacija (BAM) ', 'has_tool' : 'true', 'tool_value': 'Iznos koji je uplačen kao uplata poreza tokom poreznog perioda'})
        $('#fields-21-name').attr({'read_label': 'Mjesecni iznos akontacije', 'has_tool': 'true', 'tool_value': ' Iznos koji bi se mjesečno uplačivao tokom poreznog perioda kao akontacija'}).css('background', 'lightgray')
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
        autoclose: true,
        format: "mm",
        viewMode: "months",
        minViewMode: "months",
    }).on('changeDate', function (e) {
        var minDate = new Date(e.date.valueOf());
        $('#fields-4-name').datepicker('setStartDate', minDate);
    });

    $("#fields-4-name").datepicker({
        autoclose: true,
        format: "mm",
        viewMode: "months",
        minViewMode: "months",
    });

    $('#fields-22-name').datepicker({
        format: 'dd.mm.yy'
    })

  
    $('.next').fadeOut()
    

    if ($('#fields-22-name').val().length != 0) {
        $('#fields-22-name').prop('disabled', true)
    }


    $(function () {
        $('#msform :input').each(function (k,v) {
            if ($(v).attr('has_tool')) {
                const title = $(v).attr('tool_value')
                $(v).before('<i class="fa fa-question" data-toggle="tooltip" data-placement="top" title="'+title+'" > </i>')
                $('[data-toggle="tooltip"]').tooltip()
            }
        })
    })

});

$(function () {
    $("#msform :input").on('change keyup input', function () {
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
        if ($('#fields-5-name').val().length === 0 && $('#fields-6-name').val().length === 0) {
            console.log('a')
            $('.next').fadeOut()
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
            console.log('a')
        }
    }
    else {
        
        $('.next').fadeIn()
        $('.error').remove()
    }
});

