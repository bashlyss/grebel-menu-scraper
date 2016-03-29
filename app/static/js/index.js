$(document).on('click', '.preference .delete', function () {
    var prefId = $(this).parent().data('id');
    var $self = $(this);
    $.ajax({
        url: 'preferences/' + prefId,
        type: 'DELETE',
        success: function(result) {
            $self.parent().remove();
        }
    });
});

$(document).ready(function () {
    $("#add-preference-form").submit(function (event) {
        $.post($(this).attr('action'), $(this).serialize(), function (res) {
            $prefList = $("#preferences > ul")
            $newItem = $("<li>").addClass('preference').data('id', res.id)
            $newItem.append($("<span>").text(res.food));
            $newItem.append($("<button>").addClass("delete u-pull-right link").text("X"));
            $prefList.append($newItem);
        });
        event.preventDefault();
    });
});
