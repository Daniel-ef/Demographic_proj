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



function go() {
    var host = document.location.host;
    var req = getXmlHttp();
    req.open('POST', 'http://' + host + '/req_comment', true);
    req.setRequestHeader("Content-type","application/json");
    req.setRequestHeader("Accept-Languege", "en-US,en, ru;q=0.5");
    var comment_text = $('#comment_form').val();
    var groups = '';
    if (document.getElementById('groups_form').style.display != 'none')
        groups = $('#groups_form').val();
    req.onreadystatechange = function() {
        if (req.readyState == 4) {
            if(req.status == 200) {
                document.getElementById('btn_result').textContent='Success!';
                alert(JSON.parse(req.responseText)['result']['prediction']);
                setTimeout(function() {
                    document.getElementById('btn_result').textContent='Go!';
                }, 2000)
            }
        }
    };
    req.send(JSON.stringify([comment_text, groups]));
}
