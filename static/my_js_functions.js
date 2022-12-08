//Cuando el documento carga, se muestra la funcion
//$(document).ready(function () {
$(document).ready(function () {
    $('#abrir_modal').click(function(){
        $('.ui.modal').modal('show');
        
    })
    
    $('#tag_play_scene').click(function(){
        var texto_modal =  $('#tag_input_modal').val(); 
        
        console.log(texto_modal);
        
        $.ajax({
            url: "/play_recording/" + texto_modal,
            type: "GET",
            contentType: "application/json"
            
        })
    })
    
    // Click cerrar modal alerta
    $('#close_modal_button').click(function(){
        $('#modal_alert').modal('hide');
    })
    
    //Dropdown
    $('#select-scene-to-record').dropdown({allowAdditions: true});
    $('#select-universe-number').dropdown({allowAdditions: true});
    
    
    
});

// Nos manda a una pagina, recibe la pagina a la que vamos
function go_to_page(page_to_go){
    var base_url = window.location.origin;
    var url_to_go = base_url.concat(page_to_go);
    console.log(url_to_go);
    window.open(url_to_go, "_self");
    
    
}


// Reproduce una escena, recibe la escena a reproducir
function play_scene(scene_to_play){
    var xhttp = new XMLHttpRequest();
    var url = "/play_recording/";
    url = url.concat(scene_to_play);
    
    
    
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            //alert(this.responseText);
            message_response = JSON.parse(this.responseText).message;
            message_response = JSON.stringify(message_response);
            alert(message_response);
        }
    };
    xhttp.open("GET", url, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
    
}

// Para broadcast de grabacion
function stop_broadcast(){    
    var xhttp = new XMLHttpRequest();
    var url = "/stop_broadcasting/"
    
    console.log("Paramos grabacion")
    
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            //alert(this.responseText);
            message_response = JSON.parse(this.responseText).message
            message_response = JSON.stringify(message_response);
            alert(message_response);
        }
    };
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
    
}

//funcion que llama endpoint de grabación
function get_record_dropdown_value(){
    
    var x = $('#select-universe-nomber').dropdown('get value');
    x = from_html_to_text(x);
    console.log(x);
    
}

function from_html_to_text(html_text){
    var span = document.createElement('span');
    span.innerHTML = html_text;
    html_text = span.innerText;
    
    return html_text;
}

//Llama a endpoint de empezar grabación
function call_record_endpoint(url){
    var scene_number = $('#select-scene-to-record').dropdown('get value');
    var universes = $('#select-universe-number').dropdown('get value');
    scene_number = from_html_to_text(scene_number);
    universes = from_html_to_text(universes);
    request_body = {
        "scene_number": scene_number,
        "universes": universes
    };
    
    if(scene_number != '' && universes != ''){
        post_request(url, request_body);
    }
    else{
        alert("Please select scene and universe");
    }
}

//Llama endpoint de delete
function call_delete_scene_endpoint(scene_to_delete){
    var url = '/delete_scene/';
    url = url.concat(scene_to_delete);
    // Reconfirmamos que se quiere borrar
    x = window.confirm("Estas seguro de que quieres borrar la scene_".concat(scene_to_delete));
    if (x == true){
        delete_request(url)
        location.reload()
    }
    else{
        return
    }
}

// Makes a post request
function post_request(url, request_body){
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

// Makes a delete request
function delete_request(url){
    $.ajax({
        url: url,
        type: 'DELETE',
        contentType: 'application/json',
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



