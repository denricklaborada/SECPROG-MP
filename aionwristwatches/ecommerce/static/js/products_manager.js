$(document).ready( function() {

    var btnDelete = $("#btnDelete");

    btnDelete.on("click", function () {
        ids = get_checked();

        if (ids.length > 0) {
            $.ajax({
                url: "/prodman/delete/",
                data: { "ids[]": ids },
                success: function (response) {
                    if (response === 'Success')
                        location.reload();
                }
            })
        }
    });
});

function get_checked () {
    var checkboxes = $("input[type=checkbox]");
    var ids = [];

    for (var i = 0; i < checkboxes.length; i++) {
        if ($(checkboxes[i]).attr("data-type") === "check_product" && $(checkboxes[i]).prop('checked')) {
            ids.push($(checkboxes[i]).attr("data-id"));
        }
    }

    return ids;
}