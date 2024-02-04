// Event Delegation and DOM Traversal to add and modify components

$(document).ready(function () {

    // Using Event Delegation to update/modify existing element and adding new element by changing the source
    // attribute of an image in the main preview part when user hovers over image in a set of image previews

    $(".image-preview").on("mouseenter", ".box-preview img", function () {
        var src = $(this).attr("src");
        $(".main-image-preview .box-preview img").attr("src", src);
    });

    // Using DOM Traversal to add and modify element. Clicking on ring-size and add to cart works saying Added  
    // to cart successfully. If no ring-size is select Add to Bag will be disabled asking to select a ring-size

    $('input[name="ring-size"]').change(function () {
        var addToBagButton = $(".add-bag-page");
        var textSuccessful = $("#text-successful");

        // Clear output text when ring-size is selected
        textSuccessful.text("");

        if ($(this).is(':checked')) {

            // Ring size is selected, enabling "Add to Bag" button
            addToBagButton.removeClass("disabled").removeAttr("disabled");
        } else {
            // When no ring size is selected, disabling "Add to Bag" button
            addToBagButton.addClass("disabled").prop("disabled", true);
        }
    });

    $(".add-bag-page").click(function () {
        var addToBagContainer = $(this).parent();
        var ringSizesContainer = addToBagContainer.prev();
        var selectedRingSize = ringSizesContainer.find('input[name="ring-size"]:checked');
        var addToBagButton = $(this);
        // Output text based on whether ring is selected or not selected
        if (selectedRingSize.length === 0) {
            $("#text-successful").text("Please select a ring size before adding to the bag.");
            addToBagButton.addClass("disabled");
        } else {
            $("#text-successful").text("Added to the bag successfully.");
            addToBagButton.removeClass("disabled");
        }
    });

// Retrieving other blog posts using AJAX calls
$('.other-blogs').on('click', function() {
        $.ajax({
            url: '/other_blogs/',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                var blogsData = $('.post-details');
                blogsData.empty();
                $.each(data.blogs, function(index, blog) {
                    var blogData = `<p>${blog.description}</p>`;
                    blogsData.append(blogData);
                });
                blogsData.show();
                $('.other-blogs').hide()
                $('.hide-blogs').show()
            },
        });
});

$('.hide-blogs').on('click', function() {
    $('.other-blogs').show();
    $('.post-details').hide();
    $('.hide-blogs').hide();
});

// Writing a review for an item in the item page
$(".ask-question").click(function () {
        $(".form-review-details").show();
});
    $(".form-review-details").submit(function (e) {
    e.preventDefault();
    var ring_id = $(this).find("input[name='rings_id']").val();
    var author = $(this).find("input[name='author']").val();
    var title = $(this).find("input[name='title']").val();
    var content = $(this).find("textarea[name='content']").val();
    $.ajax({
        type: "POST",
        url: `/items/${ring_id}`,
        data: $(this).serialize(),
        success: function (response) {
            $("body").html(response);}
        });
    });

     $(".review-delete-new").on("click", function () {
        var $element = $(this);
        var reviewId = $(this).data("reviewid");
        var itemId = $(this).data("itemid");
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: "/items/" + itemId + "/delete_review/" + reviewId + '/',
            method: "POST",
            data: {
                review_id: reviewId,
                item_id: itemId,
            },
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function (response) {
                if (response.success) {
                    $element.closest('.review-discussion').remove();
                            location.reload();
                }
            },
        });
    });
});
