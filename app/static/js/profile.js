$(document).ready(function () {
  $("#table_filter").yearpicker({
    startYear: 2000,
    endYear: 2021,
  });

  $(".profile-data").hide();
});

$(function () {
  $("#searchBtn").on("click", function (e) {
    $("#add_to").empty();
    $.ajax({
      url: "/livesearch",
      method: "POST",
      data: JSON.stringify({ year: $("#table_filter").val() }),
      dataType: "json",
      contentType: "application/json",
      success: function (data) {
        dataChart(data);
      },
      error(xhr) {
        if (xhr.status == 404) {
          $("#add_to").append(
            '<div class="container">' +
              '<h1 class="text-center">Ne postoje podaci vezani za ovu godinu !</h1>' +
              "</div>"
          );
        }
      },
    });
    e.preventDefault();
  });
});

function make_subform(val, name, id, date) {
  var tag = "subform_" + val;
  var url = "";
  var img = "";
  if (name.name === "PRIM-1054") {
    url = "/render_1054/";
    edit_url = "/edit-1054/";
    delete_url = "/delete/";
    img = "/static/img/prvi-page-001.jpg";
    text = "Pregled prihoda i rashoda od iznajmljivanja  imovine ";
  } else {
    url = "/render_pr1/";
    edit_url = "/edit-pr1/";
    delete_url = "/delete/";
    img = "/static/img/drugi-page-001.jpg";
    text = "Prijava za razrez poreza na imovinu za pravna i fizicka lica";
  }
  var el = ` <div class="col-md-6 col-lg-4 pb-3" data-aos="fade-up" data-aos-duration="1000">
              <div class="card card-custom bg-white border-white border-0">
          <div class="card-custom-img" style="background-image: url(/static/img/prvi-page-001.jpg); background-size: contain;"></div>
          <div class="card-custom-avatar">
            <img class="img-fluid" src="/static/img/ProfileLogo.png" alt="Avatar" />
          </div>
          <div class="card-body" style="overflow-y: auto">
            <h4 class="card-title">${name}</h4>
            <p class="card-text"> ${text} <br>
              <br>        
              <br><br>
              Datum prijave: ${date}
          </div>
          <div class="card-footer" style="background: inherit; border-color: inherit;">
            <a href="${url + id}" class="btn btn-primary">Download</a>
            <a href="${
              edit_url + id
            }" class="btn btn-outline-primary">Izmijeni</a>
            <a href="${
              delete_url + id
            }" class="btn btn-outline-danger">Obriši</a>
          </div>
        </div>
    `;
  var $el = $(el);
  $el.data("value", val);
  return $el;
}

function dataChart(value) {
  if (value.name) {
    var i = 0;
    for (i = 0; i < value.name.length; i++) {
      $("#add_to").append(
        make_subform(i, value.name[i], value.id[i], value.date[i])
      );
    }
  }
}

$(function () {
  $(".profil").on("click", function () {
    $(".porez-data").hide();
    $(".searchFilter").hide();
    $(".profile-data").show();
  });
  $(".porez").on("click", function () {
    $(".profile-data").hide();
    $(".porez-data").show();
    $(".searchFilter").show();
  });
});
