$("#image_1").change(function() {
    sendImage();
});

var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');

function sendImage() {
    $('#text_ai').text('');
    $('#pic_ai').text('');
    
    console.log("токен в funk " + $crf_token );
    let maxFileSize = 5242880;

    img = $("#image_1")[0].files[0];

    var formData = new FormData();

    if (img.size > maxFileSize) {
        window.alert('Слишком большой файл. Размер файла не может превышать 4,5 Мб');
        return;
    }

    if (img.type != 'image/jpeg') {
        window.alert('Указанный файл не является изобр ажением в формате PNG. Передан формат '+ img.type);
        return;
    }

    formData.append('image', img);
    formData.append('key', "---44---");

    $.ajax({
        url: 'predict_image',
        type: 'POST',
        dataType: 'json',
        data: formData,
        contentType: false,
        processData: false,
        headers:{"X-CSRFToken": $crf_token},
        success: function (data) {
            console.log('Загрузка прошла удачно')
            console.log(data);

            $('#text_ai').text(data.answer);
            $('#pic_ai').html('<img src="'+data['image_link']+'">');
            $('#pic_source').html('<img src="'+data['image_source_link']+'">');
        },
        error: function(jqxhr, status, errorMsg) {
            console.log("Ошибка загрузки данных: "+errorMsg)
        }
    });

    //console.log(img);
}
