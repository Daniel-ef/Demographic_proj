function getXmlHttp(){
  var xmlhttp;
  try {
    xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
  } catch (e) {
    try {
      xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    } catch (E) {
      xmlhttp = false;
    }
  }
  if (!xmlhttp && typeof XMLHttpRequest!='undefined') {
    xmlhttp = new XMLHttpRequest();
  }
  return xmlhttp;
}


function show_groups_form() {
    if (document.getElementById('file_form').style.display != 'none') {
        $("#file_form").hide("slow", function () {} );
    }
    $("#groups_form").show("slow", function () {});
}


function show_file_form() {
    if (document.getElementById('groups_form').style.display != 'none') {
        $("#groups_form").hide("slow", function () {} );
    }
    $("#file_form").show("slow", function () {});
}


function hide_all () {
    if (document.getElementById('groups_form').style.display != 'none') {
        $("#groups_form").hide("slow", function () {
        });
    } else if (document.getElementById('file_form').style.display != 'none') {
        $("#file_form").hide("slow", function () {} );
    }

}


function check_areas() {
    if (!$('#clf_age').is(':checked') && !$('#clf_sex').is(':checked') && !$('#clf_edu').is(':checked')) {
        $('#check_clfs').show("slow", function () {});
        return false;
    } else {
        if (!$('#check_clfs').is(":hidden"))
            $('#check_clfs').hide("slow", function () {});
    }
    if ($('#comment_form').val() == '') {
        $('#check_text').show("slow", function () {
            if ($('#radio_groups').is(":checked"))
                if ($('#groups_form').val() == '')
                    $('#check_groups').show("slow", function () {
                    });
                else
                    $('#check_groups').hide("slow", function () {
                    });
        });
        return false;
    } else {
        if ($('#check_text').is(':hidden') == false) {
            $('#check_text').hide("slow", function () {
                if ($('#radio_groups').is(":checked"))
                    if ($('#groups_form').val() == '') {
                        $('#check_groups').show("slow", function () {
                            return false;
                        });
                    } else {
                        $('#check_groups').hide("slow", function () {
                        });
                    }
            });
        }
    }
    return true;
}


function send_req() {
    var host = document.location.host;
    var req = getXmlHttp();
    req.open('POST', 'http://' + host + '/req_comment', true);
    req.setRequestHeader("Content-type","application/json");
    req.setRequestHeader("Accept-Languege", "en-US,en, ru;q=0.5");

    var comment_text = $('#comment_form').val();
    var clfs_list = [];
    if ($("#clf_sex").is(":checked"))
        clfs_list.push("clf_sex");
    if ($("#clf_age").is(":checked"))
        clfs_list.push("clf_age");
    if ($("#clf_edu").is(":checked"))
        clfs_list.push("clf_edu");

    var groups_list = [];
    if (document.getElementById('groups_form').style.display != 'none')
        groups_list = ($('#groups_form').val()).split('\n');


    req.onreadystatechange = function() {
        if (req.readyState == 4) {
            if(req.status == 200) {
                $('#btn_result').slideUp("slow", function() {
                    $('#btn_success').show("slow");
                });
            }
        }
    };
    req.send(JSON.stringify({comments: comment_text, groups: groups_list, clfs: clfs_list}));
}


function go() {
    if (check_areas()) {
        send_req();
        document.getElementById('btn_result').textContent = 'Please, Wait...';
    }
}
