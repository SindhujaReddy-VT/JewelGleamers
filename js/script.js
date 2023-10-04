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
        var addToBagButton = $(".add-bag");
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

    $(".add-bag").click(function () {
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
});





