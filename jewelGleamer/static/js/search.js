    $(document).ready(function() {
        $('.search-form').submit(function(event) {
            event.preventDefault();
            var searchInput = $('#search-input').val().toLowerCase();
            console.log(searchInput)
            $.ajax({
            type: 'GET',
            url: '/items/search',
            data: { 'search-input': searchInput },
            success: function(response) {
                handleSearchResults((response));
            },
            error: function(error) {
                console.error('Error during search:', error);
            }
        });
        });
        function handleSearchResults(response) {
    if (response.type === 'rings') {
        $('#no-search-products').hide();
        $('#rings-div-search').show();
    } else if (response.type === 'none') {
        $('#no-search-products').show();

    }
}
    });
