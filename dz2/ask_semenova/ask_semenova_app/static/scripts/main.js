/**
 * Created by kate on 07.12.16.
 */

$(function() {
    $('body').on('click', '.ask-like_question', function(event) {
        var id = $(this).attr('question_id');
        var type = $(this).attr('like_type');
        ($('[question_id="' +id+ '"]'))[0].setAttribute('disabled', '');
        ($('[question_id="' +id+ '"]'))[1].setAttribute('disabled', '');
        event.preventDefault();
        $.ajax({
            headers: { "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()},
            url: "/like/",
            type: 'POST',
            data: {
                'id': id,
                'object':'question',
                'type': type,
            },
            success: function (data) {
                ($('[question="' +id+ '"]'))[0].innerHTML = data.rating;
            }
        });
    });
});




$(function() {
$('body').on('click', '.ask-button_ask_js', function(event) {
         event.preventDefault();
         console.log("OK");

        var title = $('.ask-form_title')[0];
        var text = $('.ask-form_text')[0];
        var tags = $('.ask-form_tags')[0];
        var error = 0;

        if( title.value == "" ) {
            $('.title_error')[0].innerHTML = "This field is required";
            error = 1;
        }

        if( text.value == "" ) {
            $('.text_error')[0].innerHTML = "This field is required";
            error = 1;
        }

        if( tags.value == "" ) {
            $('.tags_error')[0].innerHTML = "This field is required";
            error = 1;
        }


        if( error == 0) {
            $.ajax({
                headers: {"X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()},
                url: "/ask/",
                type: 'POST',
                data: {
                    'title': title.value,
                    'text': text.value,
                    'tags': tags.value,
                },
                success: function (data) {
                    title.value = "";
                    text.value = "";
                    tags.value = "";
                    $('#myModal').modal('hide');
                }
            });
        }
    })
});


$(function() {
    $('body').on('click', '.ask-like_answer', function(event) {
        var id = $(this).attr('answer_id');
        var type = $(this).attr('like_type');
        ($('[answer_id="' +id+ '"]'))[0].setAttribute('disabled', '');
        ($('[answer_id="' +id+ '"]'))[1].setAttribute('disabled', '');
        event.preventDefault();
        $.ajax({
            headers: { "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()},
            url: "/like/",
            type: 'POST',
            data: {
                'id': id,
                'object': 'answer',
                'type': type,
            },
            success: function (data) {
                ($('[answer="' +id+ '"]'))[0].innerHTML = data.rating;
            }
        });
    });


    $('body').on('click', '.ask-is_correct', function(event) {
        //event.preventDefault();
        var id = $(this).attr('answer_id');

        $.ajax({
            headers: { "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()},
            url: "/set_correct/" + id + "/",
            type: 'POST',
            data: {
            },
            success: function (data) {
                if (data.status == 'error') {
                    console.log('error');
                }
                else {
                    console.log("OK");
                }
            }
        });
    });





});


