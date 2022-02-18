/*!
 * Pawpharos Forms Library
 *
 * Date: 2022-14-03
 */

var currentForm = ""

function loadFormTemplate(target, form, template){
    $.get("/api/forms/" + form, {t: template}, function (data){
        $(target)[0].innerHTML = data.formHTML
    })
}

function toggleOffCanvas(target){
    $(target)[0].classList.toggle("show")
}

function showAddDevice() {
    if(currentForm != "AddDeviceForm"){
        loadFormTemplate("#formCanvasBody", "AddDeviceForm", "add-device-form");
        $("#formCanvasLabel")[0].innerHTML = "Add New Device";
        currentForm = "AddDeviceForm"
    }
    //toggleOffCanvas("#offCanvasElement")
}
