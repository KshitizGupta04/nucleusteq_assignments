function clearErrors(...ids) {

    ids.forEach(id => {

        const el =
            document.getElementById(id);

        if (el) el.innerText = "";
    });
}

function setError(id, message) {

    const el =
        document.getElementById(id);

    if (el) el.innerText = message;
}

function validateEmail(email) {

    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        .test(email);
}

function validatePhone(phone) {

    return /^[0-9]{10}$/
        .test(phone);
}

function validatePassword(password) {

    if (password.length < 6)
        return "Password must be at least 6 characters";

    if (password.includes(" "))
        return "Password cannot contain spaces";

    if (!/[A-Z]/.test(password))
        return "Password must contain one uppercase letter";

    if (!/[0-9]/.test(password))
        return "Password must contain one number";

    return null;
}

function validatePositiveNumber(value) {

    return !isNaN(value)
        && parseFloat(value) > 0;
}

function validatePositiveInteger(value) {

    return !isNaN(value)
        && parseInt(value) > 0;
}

// FUTURE DATE TIME VALIDATION
function validateFutureDateTime(
    date,
    time
) {

    const selected =
        new Date(`${date}T${time}`);

    return selected > new Date();
}