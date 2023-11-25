$(function() {
    var autocompleteUrl = $('#id_text').data('autocomplete-url'); // Получаем URL из данных поля

    $('#id_text').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: autocompleteUrl,
                data: {
                    term: request.term
                },
                dataType: 'json',
                success: function(data) {
                    response(data);
                }
            });
        },
        minLength: 2,  // Минимальная длина строки для начала поиска
        select: function(event, ui) {
            $('#id_text').val(ui.item.value);
            return false;
        }
    });
});