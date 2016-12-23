/**
 * Created by kate on 22.12.16.
 */
$( function () {
    var id = $('[question]')[0].getAttribute('question');
    var next_page = $('.ask-answer_container').length / 4  + 1;
    $(window).scroll(function () {
        if ($(window).height() + $(window).scrollTop() >= $(document).height()) {
            next_page = $('.ask-answer_container').length / 4  + 1;
            console.log("AJAX!");
            $.ajax({
            headers: { "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()},
            url: "/question/"+id.toString()+"/?page="+next_page.toString(),
            type: 'GET',
            data: {
            },
            success: function (data) {
                console.log("DONE");
                var empty = $('.answers_empty')[0];
                var new_node = document.createElement('div');
                new_node.innerHTML = data;
                empty.parentNode.appendChild(new_node);

            }
            });
        }
    });
})