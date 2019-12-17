$(function () {
    var $dehaze = $('#dehaze');
    var $real = $('#real');
    var $result = $('#result');
    var $loading = $('#loading');

    // Activate tooltip
    $('[data-toggle="tooltip"]').tooltip();

    $dehaze.on('click', function (e) {
        e.preventDefault();
        console.log('report');
        document.getElementById('loading').style.visibility = 'visible';
        dehazeImage();
    });

    function dehazeImage() {
        var form = document.querySelector('#image-form');
        var formData = new FormData(form);
        $.ajax({
            url: "/dehaze",
            data: formData,
            type: 'POST',
            contentType: false,
            cache: false,
            processData: false,
            async: false,
            success: function (response) {
                document.getElementById('loading').style.visibility = 'hidden';
                console.log(response['real']);
                $real.attr("src",  response['real']);
                $result.attr("src", response['dehazed']);
                return true;
            }
        });
    }

});
