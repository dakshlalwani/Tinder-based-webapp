$(document).ready(function () {

    $('.form').find('input, textarea').on('keyup blur focus mouseup', function (e) {

        var $this = $(this),
            label = $this.prev('label');

        if (e.type === 'keyup' || e.type === 'mouseup') {
            if ($this.val() === '') {
                label.removeClass('active highlight');
            } else {
                label.addClass('active highlight');
            }
        } else if (e.type === 'blur') {
            if ($this.val() === '') {
                label.removeClass('active highlight');
            } else {
                label.removeClass('highlight');
            }
        } else if (e.type === 'focus') {

            if ($this.val() === '') {
                label.removeClass('highlight');
            }
            else if ($this.val() !== '') {
                label.addClass('highlight');
            }
        }

    });
});