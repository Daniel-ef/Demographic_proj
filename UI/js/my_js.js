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


// Focus on comment_form
$(document).ready(function() {
    $("#btn_comment").click(function () {
        if (document.getElementById('groups_form').style.display != 'none')
            $("#groups_form").hide("slow", function () {});
        else if (document.getElementById('file_form').style.display != 'none')
            $('#file_form').hide("slow", function() {});

        if (document.getElementById('comment_form').style.display != 'none') {
            document.getElementById('comment_form').textContent = '';
        } else {
            $("#comment_form").show("slow", function () {
                document.getElementById('comment_form').textContent = 'Write comment';
            });
        }
    });
});


$(document).ready(function() {
    $("#btn_groups").click(function () {
        if (document.getElementById('file_form').style.display != 'none')
            $('#file_form').hide("slow", function() {});
        else if (document.getElementById('comment_form').style.display != 'none')
            $('#comment_form').hide("slow", function() {});

        if (document.getElementById('groups_form').style.display != 'none') {
            document.getElementById('groups_form').textContent = '';
        } else {
            $("#groups_form").show("slow", function () {
                document.getElementById('groups_form').textContent = 'Write groups (-group_number)';
            });
        }
    });
});


$(document).ready(function() {
    $("#btn_file").click(function() {
        if (document.getElementById('groups_form').style.display != 'none')
            $("#groups_form").hide("slow", function () {});
        else if (document.getElementById('comment_form').style.display != 'none')
            $('#comment_form').hide("slow", function() {});
        $("#file_form").show("slow", function(){});
    });
});


function go() {
    var host = document.location.host;
    var req = getXmlHttp();
    req.open('POST', 'http://' + host + '/req_comment', true);
    var comment_text = document.getElementById('comment_form').textContent;
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
    req.send(comment_text);
}
