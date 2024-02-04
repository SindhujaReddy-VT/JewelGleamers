function confirmDelete(ringId) {
        if (confirm("Are you sure you want to delete this product?")) {
            document.querySelector(`form[action*="${ringId}"]`).submit();
        }
    }

 function sortByPrice() {
    var itemContainer = $(".grid-images");
    var items = itemContainer.find(".image-containers");
    items.sort(function(p1, p2) {
        var price1 = parseFloat($(p1).data("price"));
        var price2 = parseFloat($(p2).data("price"));
        return price1 - price2;
    });
    items.detach().appendTo(itemContainer);
}

    $(document).ready(function () {
        $(".generate-description").on("click", function () {
            var itemId = $(this).data("itemid");
            var prompt = $(".prompt").val();
            var csrfToken = $("input[name='csrfmiddlewaretoken']").val();
            style = "display: none;"
            $.ajax({
                type: "POST",
                url: "/generate_description/" + itemId + "/",
                data: { csrfmiddlewaretoken: csrfToken, prompt: prompt },
                success: function (response) {
                    if (response.success) {
                        console.log("Testing SUCCESS");
                        $("#description-edit").val(response.enhanced_description);
                        $("#description-content").hide();
                        $("#save-description").show();
                        $("#description-edit").css("display", "block");
                        $("#cancel-description").show()
                        $(".generate-placeholder").css("display", "block");
                        $(".prompt-error").hide()
                        $(".description-error").hide()
                        $("#rate-limit-error").text("Rate limit reached. Please try again after a short wait of 1 minute.").hide();
                    } else {
                        console.error(response.error);
                        $(".prompt-error").show()
                        $(".prompt-error").html("Prompt cannot be empty! Please enter a valid prompt").css("color", "red")
                    }
                },
                error: function(xhr, status, error) {
                         if (xhr.status === 429) {
                             $("#rate-limit-error").text("Rate limit reached. Please try again after a short wait of 1 minute.").show();
                             $("#description-content").hide();
                             $("#save-description").hide();
                             $("#description-edit").hide();
                             $("#cancel-description").hide();
                             $(".generate-placeholder").css("display", "none");
                             $(".prompt-error").hide();
                             $(".description-error").hide();

                         } else {
                            console.error("AJAX Error:", status, error);
                         }
                }
            });
        });

        $("#save-description").on("click", function () {
            var editedDescription = $("#description-edit").val();
            var itemId = $(this).data("itemid");
            var csrfToken = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax({
                type: "POST",
                url: "/save_description/" + itemId + "/",
                data: { csrfmiddlewaretoken: csrfToken, 'edited_description': editedDescription },
                success: function (response) {
                    if (response.success) {
                        console.log(response.enhanced_description)
                        $(".description-new").html(response.enhanced_description);
                        console.log("Description saved successfully");
                        $("#description-content").html(editedDescription).show();
                        $("#description-edit").hide();
                        $("#save-description").hide();
                        $("#cancel-description").hide();
                        $(".generate-placeholder").css("display", "none");
                        $(".description-error").hide()
                        $(".prompt-error").hide()
                    } else {
                        console.error(response.error);
                        $(".description-error").show()
                        $(".description-error").html("Description cannot be empty! Please enter a description or regenerate.").css("color", "red")
                    }
                },
                error: function () {
                    console.error("Failed to communicate with the server.");
                }
            });
        });

        $("#cancel-description").on("click", function () {
            $("#description-edit").hide();
            $("#save-description").hide();
            $("#cancel-description").hide();
            $(".generate-placeholder").css("display", "none");
            $(".prompt-error").hide()
            $(".description-error").hide()
        });
    });
