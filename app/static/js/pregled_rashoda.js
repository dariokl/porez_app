$('#fields-0-name').prop( "disabled", true )
$('#fields-4-name').val('(Porezni period (do))')
var li = [$('#fields-8-name').val(), $('#fields-9-name').val(), $('#fields-10-name').val(), $('#fields-11-name').val(), $('#fields-12-name').val(), $('#fields-13-name').val(), $('#fields-14-name').val()]
var total = 0
for (var i = 0; i < li.length; i++) {
    total += li[i] << 0;
}
$('#fields-17-name').val(total)
