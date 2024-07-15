function delete_event(item_id) {
    console.log("delete_event", item_id)
    // AJAX request to perform the action
    jQuery.ajax({
        type: 'POST',
        url: '/delete_event',
        data: {
            item_id
        },
        success: function (response) {
            console.log('event deleted successfully:', response);
            window.location.reload();
        },
        error: function (error) {
            console.error('Error deleteing event form:', error);
        }
    });
}

function submit_event() {
    const log_name = document.getElementById('log_name').value;
    const log_type = document.getElementById('log_type').value;

    // AJAX request to submit the form data
    jQuery.ajax({
        type: 'POST',
        url: '/submit_new_log',
        data: {
            name: log_name,
            log_type
        },
        success: function (response) {
            console.log('Form submitted successfully:', response);
            window.location.reload();
        },
        error: function (error) {
            console.error('Error submitting form:', error);
        }
    });

    // Close the modal after submission
    $('#exampleModal').modal('hide');

}