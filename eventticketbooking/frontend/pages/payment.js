const token =
    localStorage.getItem("token");

if (!token) {

    window.location.href =
        "login.html";
}


// ======================================
// ERROR HELPERS
// ======================================

function showFieldError(id, message) {

    document.getElementById(
        `${id}Error`
    ).textContent = message;
}

function clearErrors() {

    document.querySelectorAll(
        ".error-text"
    ).forEach(error => {

        error.textContent = "";
    });
}


// ======================================
// VALIDATION
// ======================================

function validateCardName(name) {

    return /^[A-Za-z ]{3,}$/.test(name);
}

function validateCardNumber(number) {

    return /^\d{16}$/.test(number);
}

function validateExpiry(expiry) {

    if (

        !/^(0[1-9]|1[0-2])\/\d{2}$/
            .test(expiry)
    ) {

        return false;
    }

    const [month, year] =
        expiry.split("/");

    const expiryDate = new Date(
        2000 + parseInt(year),
        parseInt(month)
    );

    return expiryDate > new Date();
}

function validateCVV(cvv) {

    return /^\d{3}$/.test(cvv);
}


// ======================================
// AUTO FORMAT CARD NUMBER
// ======================================

document.getElementById(
    "cardNumber"
).addEventListener("input", function () {

    this.value = this.value

        .replace(/\D/g, "")

        .slice(0, 16);
});


// ======================================
// AUTO FORMAT EXPIRY
// ======================================

document.getElementById(
    "expiry"
).addEventListener("input", function () {

    let value = this.value

        .replace(/\D/g, "");

    if (value.length >= 3) {

        value =

            value.slice(0, 2)

            +

            "/"

            +

            value.slice(2, 4);
    }

    this.value = value;
});


// ======================================
// AUTO FORMAT CVV
// ======================================

document.getElementById(
    "cvv"
).addEventListener("input", function () {

    this.value = this.value

        .replace(/\D/g, "")

        .slice(0, 3);
});


// ======================================
// PAYMENT SUBMIT
// ======================================

document.getElementById(
    "paymentForm"
).addEventListener("submit", async function (e) {

    e.preventDefault();

    clearErrors();

    const cardName =
        document.getElementById(
            "cardName"
        ).value.trim();

    const cardNumber =
        document.getElementById(
            "cardNumber"
        ).value.trim();

    const expiry =
        document.getElementById(
            "expiry"
        ).value.trim();

    const cvv =
        document.getElementById(
            "cvv"
        ).value.trim();


    // ======================================
    // VALIDATIONS
    // ======================================

    let isValid = true;


    if (!validateCardName(cardName)) {

        showFieldError(

            "cardName",

            "Enter valid card holder name"
        );

        isValid = false;
    }

    if (!validateCardNumber(cardNumber)) {

        showFieldError(

            "cardNumber",

            "Card number must contain exactly 16 digits"
        );

        isValid = false;
    }

    if (!validateExpiry(expiry)) {

        showFieldError(

            "expiry",

            "Enter valid expiry date (MM/YY)"
        );

        isValid = false;
    }

    if (!validateCVV(cvv)) {

        showFieldError(

            "cvv",

            "CVV must contain exactly 3 digits"
        );

        isValid = false;
    }

    if (!isValid) {

        return;
    }


    // ======================================
    // BOOKING DATA
    // ======================================

    const bookingData = JSON.parse(
        localStorage.getItem(
            "pendingBooking"
        )
    );

    if (!bookingData) {

        showToast(
            "No booking found",
            "error"
        );

        return;
    }


    // ======================================
    // MOCK PAYMENT
    // ======================================

    try {

        showToast(
            "Processing payment...",
            "info"
        );

        await new Promise(resolve =>

            setTimeout(resolve, 1500)
        );


        // ======================================
        // BOOK TICKETS
        // ======================================

        const response =

            await bookTickets(
                bookingData
            );

        showToast(
            response,
            "success"
        );

        localStorage.removeItem(
            "pendingBooking"
        );

        setTimeout(() => {

            window.location.href =
                "bookings.html";

        }, 1200);

    } catch (error) {

        showToast(
            error.message,
            "error"
        );
    }
});