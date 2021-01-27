$(document).ready(function () {
  $(".next").fadeOut();
  $('#select option[value="0"').prop("disabled select", true);

  $(function () {
    if (localStorage.getItem("cityData")) {
    } else {
      $.ajax({
        method: "POST",
        url: "/fetchcity",
        success: function (response) {
          localStorage.setItem("cityData", JSON.stringify(response));
        },
      });
    }
  });
});

function isInArray(value, array) {
  return array.indexOf(value) > -1;
}

function make_subform(val, title) {
  var tag = "subform_" + val;
  var el =
    '<div class="subform" style="display: flex; flex-direction: column;">' +
    "<h4>" +
    title +
    "</h4>" +
    "<span> Opcina </span>" +
    '<select id="' +
    tag +
    '_oname" type="text" placeholder="Lokacija imovine"></select>' +
    "<span > Adresa i Broj </span>" +
    '<input id="' +
    tag +
    '_fname" type="text" placeholder="Adresa i Broj"></input>' +
    "<span > Jedinica Mjere </span>" +
    '<input id="' +
    tag +
    '_lname" type="text" placeholder="Jedinica Mjere"></input>' +
    "<span> Broj/Jedinica Mjere </span>" +
    '<input id="' +
    tag +
    '_add1" type="text" placeholder="Broj Jedinica Mjere"></input>' +
    "<span> Iznos Poreza</span>" +
    '<input id="' +
    tag +
    '_add2" type="text" placeholder="Porez po Jedinici Mjere" disabled></input>' +
    "<span> Ukupno </span>" +
    '<input id="' +
    tag +
    '_add3" type="text" placeholder="Iznos Poreza" disabled></input>' +
    "</div>";
  var $el = $(el);
  $el.data("value", val);
  var cityArray = JSON.parse(localStorage.getItem("cityData"));
  for (i = 0; i < cityArray.length; i++) {
    $el
      .find("select")
      .append(
        '<option value="' +
          cityArray[i][0] +
          '">' +
          cityArray[i][1] +
          "</option>"
      );
  }
  $(function () {
    $("select").change(function (e) {
      for (i = 0; i < cityArray.length; i++) {
        if ($(e.target).val() === cityArray[i][0]) {
          $($el.children().eq(10).val(cityArray[i][2]));
        }
      }
    });
  });

  $(function() {
      $($el.children().eq(8)).on('keyup', function(){
        var one = $($el.find('input').eq(2))
        var two = $($el.find('input').eq(3))

        var arOne = one.get()
        var arTwo = two.get()
        $($el.children().eq(12).val(arOne[0].value * arTwo[0].value))
          
      })
  })

  return $el;
}

String.prototype.insert = function (index, string) {
  var ind = index < 0 ? this.length + index : index;
  return this.substring(0, ind) + string + this.substr(ind);
};

function check_id() {
  return $('.subform').length;
}

$('.sub_forms').on('blur', 'input', function() {
  console.log('aa')
})

$(function () {
  $("#select_type").change(function (e) {
    var value = $(e.target).val();
    var title = $(this).find("option:selected").text();
    if (check_id() !== 9) {
      $(".sub_forms").append(make_subform(value.insert(-1, check_id()), title));

    } else {
      var $div = $('<div class="mt-2 col"></div>');
      $div.css({
        background: "#FF5555",
        color: "black",
      });
      if ($("div.error", $(this).parent()).length == 0) {
        $div.html("Maksimalan broj za kategoriju nekretnine !");
        $div.addClass("error"); //could also add the above styles to your css for .error and remove that code
        $div.insertAfter($(this));
      }
    }
    $(e.target).val(0);
    $(".next").fadeIn();
  });
});

$(function () {
  $("#ajax_post").click(function (event) {
    var data_dict = {};
    $(".sub_forms")
      .children()
      .each(function (index, value) {
        var $el = $(value);
        var key = $el.data("value");
        var val = [];
        $el.find("input").each(function (_, v) {
          val.push(v.value);
        });
        data_dict[key] = val;
        console.log(key);
      });
    $.ajax({
      type: "POST",
      url: "/step_1",
      data: JSON.stringify(data_dict),
      contentType: "application/json;charset=UTF-8",
      success: function (data) {
        console.log(data);
      },
    });
    event.preventDefault();
  });
});
