/**
 * Created by kate on 20.12.16.
 */
$(function() {
    $('#search').on('input', function(event) {
        event.preventDefault();
        var input_search = $("#search").val();
        var list = document.getElementById('search_list');
        if (input_search.length >= 3 && input_search.length < 150 )
        {
            $.ajax({
                url: "/search_list/",
                type: 'GET',
                data: {
                    'text': input_search,
                },
                success: function (data) {
                    list.innerHTML = '';

                    for( var i in data.list ) {
                        var option = document.createElement('option');
                        option.value = data.list[i][1];
                        list.appendChild(option);
                        var option = document.createElement('option');
                        option.value = data.list[i][2];
                        list.appendChild(option);
                    }

                    $('#search_form')[0].setAttribute('action', '/search/'+input_search);
                    console.log("OK");
                }

            });
        }
        else
        {
        // Если ничего не найдено, то скрываем выпадающий список.
        console.log('MORE');
        }
    });

});