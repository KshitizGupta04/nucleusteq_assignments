(() => {

    const bookingToken =
        localStorage.getItem("token");

    const bookingRole =
        localStorage.getItem("role");


    // ======================================
    // AUTH CHECK
    // ======================================

    if (

        !bookingToken

        ||

        bookingRole !== "CUSTOMER"
    ) {

        showToast(
            "Access Denied",
            "error"
        );

        setTimeout(() => {

            window.location.href =
                "login.html";

        }, 800);
    }


    // ======================================
    // LOAD BOOKINGS
    // ======================================

    async function loadBookings() {

        const bookingContainer =

            document.getElementById(
                "bookingContainer"
            );

        try {

            const bookings =
                await getMyBookings();

            bookingContainer.innerHTML = "";

            if (bookings.length === 0) {

                bookingContainer.innerHTML = `

                    <div class="empty-state">

                        <h3>
                            No Bookings Yet
                        </h3>

                        <p>
                            Book an event to see it here
                        </p>

                    </div>
                `;

                return;
            }

            bookings.forEach(booking => {

                bookingContainer.innerHTML +=

                    renderBookingCard(
                        booking
                    );
            });

        } catch (error) {

            bookingContainer.innerHTML = `

                <div class="error-state">

                    <p>
                        Failed to load bookings.
                    </p>

                </div>
            `;
        }
    }


    // ======================================
    // CANCEL BOOKING
    // ======================================

    async function removeBooking(id) {

        if (!confirm(
            "Cancel this booking?"
        )) {

            return;
        }

        try {

            const response =

                await cancelBooking(id);

            showToast(
                response,
                "success"
            );

            loadBookings();

        } catch (error) {

            showToast(
                error.message,
                "error"
            );
        }
    }


    // MAKE GLOBAL FOR BUTTON
    window.removeBooking =
        removeBooking;


    // ======================================
    // INITIAL LOAD
    // ======================================

    loadBookings();

})();