const $ = window.$;
$(document).ready(function () {
    $('#myForm').on('submit', function (e) {
        e.preventDefault();
        console.log("Форма отправлена через AJAX");

        $.ajax({
            url: "{% url 'product:create_order' %}",
            type: "POST",
            data: $(this).serialize(),
            success: function (response) {
                console.log("Ответ сервера:", response);
                if (response.success) {
                    console.log("Форма прошла валидацию, закрываем модальное окно");
                    $('#exampleModal').modal('hide');
                } else {
                    console.log("Ошибки валидации:", response.errors);
                    let errorMessage = "";
                    for (let field in response.errors) {
                        errorMessage += response.errors[field].join(", ") + "\n";
                    }
                    alert("Ошибки:\n" + errorMessage);
                }
            },
            error: function () {
                console.log("Ошибка при отправке формы");
                alert('Ошибка при отправке формы!');
            }
        });
    });
});