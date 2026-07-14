export const logoutUser = (
    navigate
) => {

    localStorage.removeItem(
        "access_token"
    );

    localStorage.removeItem(
        "refresh_token"
    );

    localStorage.removeItem(
        "role"
    );


    navigate(
        "/login",
        {
            replace: true
        }
    );
};