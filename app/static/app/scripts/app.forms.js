/*!
 * Pawpharos Forms Library
 *
 * Date: 2022-14-02
 */

var currentForm = ""


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function loadFormTemplate(target, form, template, callback) {
    let url = "/api/forms/" + form + "?t=" + template;

    $.get(url, function (data){
        // Load the form data into the page
        $(target)[0].innerHTML = data.formHTML;
        // Callback occurs after the form has loaded
        callback();
    });
}

// Add Device Functions

function showRegisterDevice() {
    $('#formModal').modal('show')
}

function onAddDeviceLoad(){

    // Setup submit button
    $("#submitButton").click(function(ev) {
        let form = $("#addDevice");
        let url = form.attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(),
            success: function(data) {
                if(data.status == 1){
                    alert("Device Added!!")
                    // Clear the form to be used again
                    form[0].reset();
                }
                else{
                    $("#formCanvasBody").innerHTML = data.content;
                }
            },
            error: function(data) {
                alert("Error loading form!!");
            }
        });
    });
    
}

function unregisterDevice(ev){
        
    const csrftoken = getCookie("csrftoken") 

    $.ajax({
        type: "POST",
        url: "/api/device/remove",
        data: {
            device_id: ev.getAttribute('device'),
        },
        beforeSend: function(xhr){
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(data){
            window.location.reload()
        }
    })
}