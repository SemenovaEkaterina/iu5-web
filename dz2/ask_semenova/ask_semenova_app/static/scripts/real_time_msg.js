/**
 * Created by kate on 12.12.16.
 */

function getComet() {
    var id = $('[question]')[0].getAttribute('question');
    $.ajax({
        type: 'GET',
        url: '/listen/?cid='+id.toString(),
        success: function(data) {
            console.log("OK");
            var last_question = $('.ask-answer_container')[0];
            var new_question = last_question.cloneNode(true);
            new_question.getElementsByClassName('img-rounded')[0].setAttribute('src', data.avatar);
            new_question.getElementsByClassName('ask-rate')[0].innerHTML = data.rating;
            new_question.getElementsByClassName('ask-rate')[0].setAttribute('answer', data.id);
            new_question.getElementsByClassName('ask-answer_text')[0].innerHTML = data.text;
            new_question.getElementsByClassName('ask-like_top')[0].setAttribute('answer_id', data.id);
            new_question.getElementsByClassName('ask-like_top')[0].removeAttribute('disabled');
            new_question.getElementsByClassName('ask-like_bottom')[0].setAttribute('answer_id', data.id);
            new_question.getElementsByClassName('ask-like_bottom')[0].removeAttribute('disabled');
            new_question.getElementsByClassName('ask-is_correct')[0].setAttribute('answer_id', data.id);
            new_question.getElementsByClassName('ask-is_correct')[0].checked = false;
            last_question.parentNode.insertBefore(new_question, last_question);
            getComet();
        },
        error: function() {
       setTimeout(getComet, 10000);
        },
    });
}
getComet();