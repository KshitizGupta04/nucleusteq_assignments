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


    if (!token) {

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

        return (
            <Navigate
                to="/login"
                replace
            />
        );
    }


    return children;
}


export default ProtectedRoute;