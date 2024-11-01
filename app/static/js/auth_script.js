async function loginUser(email, password) {
    const wrongCredentialsSpan = document.getElementById("wrong_credentials");
    wrongCredentialsSpan.textContent = "";
    const url = "api/auth/login";
    await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email: email, password: password}),
    }).then(response => {
        if (response.status === 200) {
            window.location.href = "/bookings"
        } else {
            wrongCredentialsSpan.textContent = "Ошибка авторизации";
        }
    });
}

async function registerUser(email, password) {
    const wrongCredentialsSpan = document.getElementById("wrong_credentials");
    const url = "/api/auth/register";
    wrongCredentialsSpan.textContent = "";

    await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email: email, password: password}),
    })
    .then(response => {
        switch (response.status)
        {
            case 201:
                loginUser(email, password);
                break;
            case 422:
                wrongCredentialsSpan.textContent = "Некорретный email или пароль";
                break;
            case 409:
                wrongCredentialsSpan.textContent = "Пользователь уже существует";
                break;
            default:
                wrongCredentialsSpan.textContent = "Внутренняя ошибка сервера";
        }
    });
}