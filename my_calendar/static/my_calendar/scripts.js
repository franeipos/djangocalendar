function redirect_add_event(url){
    console.log(url)
    window.location = url
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
