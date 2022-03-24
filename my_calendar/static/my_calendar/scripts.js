function redirect_add_event(url){
    console.log(url)
    window.location = url
}


function send_search_request(){
    var search_text = document.getElementById('search_text').value

    var url = "https://api.arasaac.org/api/pictograms/es/search/" + search_text;

    var xhr = new XMLHttpRequest();
    xhr.open("GET", url);

    xhr.onreadystatechange = function () {
       if (xhr.readyState === 4) {
          console.log(xhr.status);
          if (xhr.status == 200){
            console.log(xhr.responseText);
            create_picto_div(xhr.responseText);
          }
          else {
            var main_div = document.getElementById('search_result');
            main_div.innerHTML = "";
            var p_error = document.createElement('p');
            p.innerHTML = "Ha ocurrido un error. Por favor, vuelva a intentarlo."
            main_div.append(p_error);
          }
       }};
    xhr.send();
}

function create_picto_div(responseText){
    var data = JSON.parse(responseText);
    console.log(data);

    // Show div that contains the pictograms.
    var main_div = document.getElementById('search_result');
    main_div.innerHTML = "";
    main_div.setAttribute('class', 'row d-flex');


    for(var i=0; i<data.length; i++){
        var id = data[i]['_id'];

        // Create div that contains the pictogram.
        var div_picto = document.createElement('div');
        div_picto.setAttribute('class', 'col-md-4 mb-3 text-center');

        // Create image with the picto.
        var img = document.createElement('img');
        img.src = 'https://static.arasaac.org/pictograms/' + id + '/' + id + '_300.png'
        img.classList.add('img-fluid');

        // Create a button to use that picto.
        var button = document.createElement('a');
        button.innerHTML = 'Seleccionar'
        button.setAttribute('class', 'btn btn-sm btn-outline-success mt-2')
        button.setAttribute('data-id', id);
        button.setAttribute('onClick', 'use_selected_picto('+id+')');

        div_picto.append(img);
        div_picto.append(button);
        main_div.append(div_picto);
        console.log(data[i]['_id']);
    }

}

function use_selected_picto(id_picto){
    console.log('Selected picto:' + id_picto);

    // Hide search form.
    var search_form = document.getElementById('search_form');
    search_form.setAttribute('class', 'd-none');

    // Hide search result and clear content.
    var search_div = document.getElementById('search_result');
    search_div.innerHTML="";
    search_div.setAttribute('class', 'row d-none');

    var main_div = document.getElementById('selected_image');

    // Create a div that contains the selected image.
    var div_image = document.createElement('div');
    div_image.setAttribute('class', 'col-md-6');

    var p_title = document.createElement('p');
    p_title.innerHTML="Imagen seleccionada:";

    // Create image with the picto.
    var picto_img = document.createElement('img');
    url_picto = 'https://static.arasaac.org/pictograms/' + id_picto + '/' + id_picto + '_300.png'
    picto_img.src = url_picto;
    picto_img.classList.add('img-fluid');

    // Create a button to cancel operation.
    var cancel_button = document.createElement('a');
    cancel_button.setAttribute('class', 'btn btn-sm btn-outline-danger');
    cancel_button.innerHTML = "Eliminar imagen";
    cancel_button.onclick = function() {clear_selected_image(1)}

    div_image.append(p_title);
    div_image.append(picto_img);
    div_image.append(cancel_button);
    main_div.append(div_image);

    // Set the url of the image in the input of the Event form.
    var url_image_input = document.getElementById('url_image');
    url_image_input.value = url_picto;

}

function clear_event_image(online){
    if(online == 0){
        // Check the box for Django removal.
        var check_del = document.getElementById('image_clear_id');
        if (check_del != null) {
            check_del.checked = true;
        }
    }
    else{

        // Remove url of the image in the input of the Event form.
        var url_image_input = document.getElementById('url_image');
        url_image_input.value = "";
    }

    var div_image = document.getElementById('event_image');
    div_image.setAttribute('class', 'd-none');

    var p_message = document.getElementById('picto_message');
    p_message.innerHTML = "Sin pictograma."

    var accordion_upload = document.getElementById('upload_image_accordion');
    accordion_upload.classList.remove('d-none');
    accordion_upload.classList.add('d-block');

}


function clear_selected_image(online) {
    if(online == 1) {
        // Remove url of the image in the input of the Event form.
        var url_image_input = document.getElementById('url_image');
        url_image_input.value = "";

        // Clear content of the selected image div.
        var div_image = document.getElementById('selected_image');
        div_image.innerHTML = "";

        // Show search form and clear search input.
        var search_form = document.getElementById('search_form');
        search_form.setAttribute('class', 'd-block');
    }
    else {
        // Remove src from the image preview element.
        var img_preview = document.getElementById('img_preview');
        img_preview.src = "";

        // Clear value from file input.
        var image_event_input = document.getElementById('input_event_image');
        image_event_input.value = "";

        // Hide the div that contains the image preview.
        var div_img_preview = document.getElementById('div_img_preview');
        div_img_preview.classList.remove('d-flex');
        div_img_preview.classList.add('d-none');

    }
}


function load_preview(event){
    // Show div that contains the image preview.
    var div_img_preview = document.getElementById('div_img_preview');
    div_img_preview.classList.remove('d-none');
    div_img_preview.classList.add('d-flex');

    // Load src to the img element for preview.
    var img_preview = document.getElementById('img_preview');
    if (event.target.files[0] != undefined){
        img_preview.src = URL.createObjectURL(event.target.files[0]);
        img_preview.onload = function() {
            URL.revokeObjectURL(img_preview.src); // free memory
        }

    var check_del = document.getElementById('image_clear_id');
        if (check_del != null) {
            check_del.checked = false;
        }
    }
    else {
        clear_selected_image(0); // if no file is selected, clear the preview and file input.
        clear_event_image(0); // if the user is updating the file, assure that the image is deleted.
    }
}

// show modal to delete patient.
$(document).on("click", ".open-delete-patient", function () {
     var patient_id = $(this).data('id');
     var patient_name = $(this).data('name');
     var delete_path = $(this).data('url');
     console.log(delete_path)
     $(".modal-body #modal-patient-name").html( patient_name );
     $(".modal-footer #modal-patient-link").attr('href', delete_path)
});
