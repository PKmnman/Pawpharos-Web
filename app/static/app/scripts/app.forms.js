/*!
 * Pawpharos Forms Library
 *
 * Date: 2022-14-02
 */

var currentForm = ""

function loadFormTemplate(target, form, template, callback){
    let url = "/api/forms/" + form + "?t=" + template;

    $.get(url, function (data){
        // Load the form data into the page
        $(target)[0].innerHTML = data.formHTML;
        // Callback occurs after the form has loaded
        callback();
    });
}

// Add Device Functions

function showAddDevice() {
    // Wrap in an if statement to prevent multiple executions
    if(currentForm != "AddDeviceForm"){
        // Set the label of the off-canvas element
        $("#formCanvasLabel")[0].innerHTML = "Add New Device";
        loadFormTemplate("#formCanvasBody", "AddDeviceForm", "add-device-form", onAddDeviceLoad);
        currentForm = "AddDeviceForm"
    }
}

function onDeviceChange(){
    elem = document.getElementById("id_device_type")
    if(elem.value == "S"){
        document.getElementById("masterToggle").removeAttribute("hidden");
    }else{
        document.getElementById("masterToggle").setAttribute("hidden", "");
    }
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
