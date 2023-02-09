$(document).ready(function () {
    
    
    // Al dar enter en el input, guarda la ip
    var input = document.getElementById("ip_input");
    input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            document.getElementById("done_button").click();
        }
    });
    
    /*
    var edit_status = 1;
    $("#edit_button").click(function(){
        if(edit_status == 1){
            $("#description_text").hide(); 
            edit_status = edit_status * -1;
        }
        else if(edit_status == -1){
            $("#description_text").show(); 
            edit_status = edit_status * -1;
        }
        
    });
    */
    $("#cancel_modal_description").click(function(){
        clear_description_var();
        $('#edit_description_modal').modal('hide');
    });
    
    // Guardar texto de form al clickear shift + Enter
    var input = document.getElementById("description_text");
    input.addEventListener("keypress", function(event) {
        if (event.key === "Enter" && !event.shiftKey ) {
            event.preventDefault();
            document.getElementById("save_description").click();
        }
    });
    
    
    436
    
 
    
});



var scene = '';
function open_description_modal(value){
    // Mostrar modal
    $('#edit_description_modal').modal('show');
    //Changes content of the element by id
    document.getElementById("change_description_header").innerHTML = "Change description ".concat(value);
    // Changes de value of the button with id "save_description", it sets it to the scene that we need
    $('#save_description').attr('data-value', value);

    scene = value;
    
}

function clear_description_var(){
    scene = '';
}

var new_description = '';
function save_scene_description(){
    var valor = document.getElementById("description_text").value;
    
    
    
    if (valor == ''){
        alert("Nothing to save");
    }else{
        // Gets "data-value" attribute of div button by its id
        var escena_a_cambiar = document.querySelector('#save_description').getAttribute("data-value");
        var request_body = {
            "scene_to_update": "scene_".concat(escena_a_cambiar),
            "description_message": valor
        }
        // lamando endpoint para cmabiar la descripcion
        post_request("/update_recording_description/", request_body);
        location.reload();

    }
    
}

function open_ip_modal(){
    // Mostrar modal
    $('#modal_cambiar_ip').modal('show');  // Cambiar ip
}


function save_new_ip(){
    var valor = document.getElementById("ip_input").value;
    var url = '/change_config_value/';
    var request_body = {
        "lista_campo": ["settings", "ip_address"],
        "value": valor
    }
    // Revisamos que el formato de la ip sea correcto
    if (ValidateIPaddress(valor)){
        console.log(url);
        console.log(request_body);
        post_request(url, request_body);

    }
}

// Revisa que el formato de la ip sea correcto
function ValidateIPaddress(ipaddress) {  
    if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ipaddress)) {  
        return (true)  
    }  
    alert("You have entered an invalid IP address!");
    return (false)  
}  


// Makes a post request
function post_request(url, request_body=''){
    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(request_body), 
        success: function (data, status, jqXHR) {
            alert(JSON.stringify(data));// write success in " "
        },
        error: function (jqXHR, status) {
            // error handler
            console.log(jqXHR);
            alert('fail' + status.code);
        }
    });
}