function registerFine() {
    swal({
        title: "Регистрация",
        text: "Вы зарегестрировались успешно!",
        icon: "success",
    });
    setTimeout(
        () => {
        window.location.href = "/login";
        }, 3000);
}

function registerBad() {
    swal({
        icon: 'error',
        title: 'Oops...',
        text: 'Что то пошло не так...'
    });
}

function GoDashbord(){
    window.location.href = '/dashbord';
}

function GoRedactorPage(){
    window.location.href = '/redactor'
}

function changeTheme(){
    window.location.href = "/changeTheme";
}

