$(document).ready(function () {

    // Navigating to the related page by finding the results on the search bar and displaying 
    // error friendly message if resultant page not found

    const searchParams = new URLSearchParams(window.location.search);

    // Taking the search input and converting it into lower case to validate
    var input = searchParams.get('search-input').toLowerCase();

    // Resultant output content to display on Search Result page
    const outputResult = $('#output-content');
    let outputContent = '';

    // Taking input from the search bar and switching accordingly to provide the output page
    switch (input) {
        case 'rings':
            window.location.href = 'category.html';
            break;
        case 'diamonds':
            outputContent = '<p>Here are your search results for : ' + input + '</p>';
            outputResult.html(outputContent);
            break;
        case 'bracelets':
            outputContent = '<p>Here are your search results for : ' + input + '</p>';
            outputResult.html(outputContent);
            break;
        case 'blog':
            window.location.href = 'blog.html';
            break;
        default: outputContent = '<h1> NO SEARCH RESULTS FOUND </h1>' +
            '<p> Navigate back to the home page and try finding other results. </p>';
            outputResult.html(outputContent);
            break;
    }
});