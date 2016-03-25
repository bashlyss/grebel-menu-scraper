$(document).on('click', '.preference .delete', function () {
    var prefId = $(this).parent().attr('data-id');
    var $self = $(this);
    $.ajax({
        url: 'preference/delete/0'.replace('0', prefId),
        type: 'DELETE',
        success: function(result) {
            $self.parent().remove();
        }
    });
});
