function registerFine() {
    swal({
        title: "Регистрация",
        text: "Вы зарегестрировались успешно!",
        icon: "success",
    });
}
function registerBad() {
    swal({
        icon: 'error',
        title: 'Oops...',
        text: 'Что то пошло не так...',
        footer: '<a href="">Why do I have this issue?</a>'
    });
}

function GoDashbord(){
    window.location.href = '/dashbord';
}

function GoRedactorPage(){
    window.location.href = '/redactor'
}

(function() {
    
        'use strict';
    
        ('.input-file').each(function() {
        var $input = $(this),
            $label = $input.next('.js-labelFile'),
            labelVal = $label.html();
        
        $input.on('change', function(element) {
            var fileName = '';
            if (element.target.value) fileName = element.target.value.split('\\').pop();
            fileName ? $label.addClass('has-file').find('.js-fileName').html(fileName) : $label.removeClass('has-file').html(labelVal);
        });
        });
    
    })();