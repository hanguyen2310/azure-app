var myCodeMirror;
var requestSend = false;
var isSending = false;

function ajaxUpdatePreview() {
    requestSend = true;
    tryAjaxUpdatePreview();
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function tryAjaxUpdatePreview() {
    if(!isSending && requestSend) {
        requestSend = false;
        isSending = true;
        var mdtext = $("#markdown_input").val()
        // console.log(mdtext);

        $.ajax({
            type: "POST",
            url: "/blog/ajax/preview/",
            headers: { "X-CSRFToken":  csrftoken },
            data: {
                "mdtext": JSON.stringify(mdtext)
            },
            dataType: "json",
            // contentType: "text/plain",
            success: function( data ) {
                console.log("request /blog/ajax/preview/ success");
                // console.log(data["html_output"]);
                isSending = false;
                setTimeout(tryAjaxUpdatePreview, 0);
                $("#html_result").html(data["html_output"]);
                var h = $("#markdown_input").height();
                $("#html_result").height(h);
            },
            error: function() {
                alert('Error occured');
            }
    });
    }
}


function updateMarkdownInput(value) {
    myCodeMirror.setValue(value);
}

var ignoreScrollEvents = false;
function syncScroll(element1, element2) {
    var ele1 = document.getElementById(element1);
    var ele2 = document.getElementById(element2);
    let maxY1 = ele1.scrollHeight - ele1.clientHeight;
    let maxY2 = ele2.scrollHeight - ele2.clientHeight;

    var ratio = maxY2 / maxY1;

    ele2.scrollTop = ele1.scrollTop * ratio;
}

$(document).ready(function() {
    // Setup custom header height
    head_height = $('#head').outerHeight(true);
    $('#mdedit').css('top', head_height+'px');
    $('#mdedit-body').css('top', (head_height+$('#mdedit').height())+'px');
    $('#markdown_input').bind('input propertychange', function(){
        // console.log(this.value);
        ajaxUpdatePreview();
    });
    console.log($('#markdown_input').scrollTop());

    $('#markdown_input').attr('onscroll', 'syncScroll("markdown_input", "html_result")');
    // $('#html_result').attr('onscroll', 'syncScroll("html_result", "markdown_input")');

    
    ajaxUpdatePreview();

});