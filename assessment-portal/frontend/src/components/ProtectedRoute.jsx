import {
    Navigate
} from "react-router-dom";


function ProtectedRoute({
    children,
    allowedRole
}) {

    const token = localStorage.getItem(
        "access_token"
    );

    const storedRole = localStorage.getItem(
        "role"
    );

    const role = storedRole
        ?.trim()
        .toLowerCase();

    const normalizedAllowedRole = allowedRole
        ?.trim()
        .toLowerCase();


    console.log(
        "PROTECTED ROUTE CHECK:",
        {
            tokenExists: Boolean(token),
            storedRole,
            normalizedRole: role,
            allowedRole:
                normalizedAllowedRole,
            currentPath:
                window.location.pathname
        }
    );


    if (!token) {

        console.error(
            "REDIRECTING TO LOGIN: No token"
        );

        return (
            <Navigate
                to="/login"
                replace
            />
        );
    }


    if (
        normalizedAllowedRole &&
        role !== normalizedAllowedRole
    ) {

        console.error(
            "REDIRECTING TO LOGIN: Role mismatch",
            {
                actualRole: role,
                expectedRole:
                    normalizedAllowedRole
            }
        );

        return (
            <Navigate
                to="/login"
                replace
            />
        );
    }


    console.log(
        "PROTECTED ROUTE: Access allowed"
    );


    return children;
}


export default ProtectedRoute;