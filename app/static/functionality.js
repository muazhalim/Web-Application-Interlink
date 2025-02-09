    // JavaScript code
    function friendRequest(username) {
        var button = $("#friendRequestButton");
        button.prop('disabled', true);
        button.hide();

        console.log("Username:", username);

        $.ajax({
            url: '/friend_request',
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            data: JSON.stringify({ username: username }),
            success: function(response) {
                console.log(response);
                button.text("Requested");

            },
            error: function(error) {
                console.log(error);
                button.prop('disabled', false);
            }
        });
    }


