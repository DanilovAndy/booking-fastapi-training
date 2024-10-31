function loginLink() {
            window.location.href = "/login"
        }

async function logoutUser() {
    const url = "/api/auth/logout";
    await fetch(url, {
        method: 'POST',
        }).then(response => {
            if (response.status === 200)
            {
                window.location.href = "/login"
            }
        });
    };

async function getUserName() {
    const url = "/api/auth/me";
    await fetch(url, {
        method: 'GET',
    })
    .then(response=>response.json())
    .then(data=>{ username = data.email; })

    if (username !== undefined) {
        requestAnimationFrame(() => {
            document.getElementById("userName").textContent = username;
            document.getElementById("authButton").textContent = "Выйти";
            });
        } else {
            document.getElementById("authButton").innerText = "Войти";
        }
    };