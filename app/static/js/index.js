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
