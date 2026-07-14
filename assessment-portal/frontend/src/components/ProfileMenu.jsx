import {
    useEffect,
    useRef,
    useState
} from "react";

import {
    FaChevronDown,
    FaEnvelope,
    FaIdBadge,
    FaUser,
    FaUserCircle
} from "react-icons/fa";

import {
    getMyProfile
} from "../services/authService";


function ProfileMenu({
    onViewProfile
}) {

    const [
        profile,
        setProfile
    ] = useState(null);


    const [
        loading,
        setLoading
    ] = useState(true);


    const [
        error,
        setError
    ] = useState("");


    const [
        menuOpen,
        setMenuOpen
    ] = useState(false);


    const menuRef = useRef(null);


    useEffect(
        () => {

            const loadProfile = async () => {

                try {

                    setLoading(true);

                    setError("");


                    const data = (
                        await getMyProfile()
                    );


                    setProfile(
                        data
                    );

                } catch (err) {

                    setError(
                        err.message ||
                        "Failed to load profile."
                    );

                } finally {

                    setLoading(false);
                }
            };


            loadProfile();

        },
        []
    );


    useEffect(
        () => {

            const handleOutsideClick = (
                event
            ) => {

                if (
                    menuRef.current &&
                    !menuRef.current.contains(
                        event.target
                    )
                ) {

                    setMenuOpen(
                        false
                    );
                }
            };


            document.addEventListener(
                "mousedown",
                handleOutsideClick
            );


            return () => {

                document.removeEventListener(
                    "mousedown",
                    handleOutsideClick
                );
            };

        },
        []
    );


    const handleToggleMenu = () => {

        setMenuOpen(
            currentValue =>
                !currentValue
        );
    };


    const handleViewProfile = () => {

        setMenuOpen(
            false
        );


        if (onViewProfile) {

            onViewProfile();
        }
    };


    const getInitial = () => {

        if (
            !profile?.username
        ) {

            return "";
        }


        return profile.username
            .charAt(0)
            .toUpperCase();
    };


    const formatRole = (
        role
    ) => {

        if (!role) {

            return "";
        }


        return (
            role.charAt(0).toUpperCase() +
            role.slice(1)
        );
    };


    return (

        <div
            className="profile-menu"
            ref={menuRef}
        >

            <button
                type="button"
                className="profile-menu-trigger"
                onClick={
                    handleToggleMenu
                }
                aria-label="Open profile menu"
                aria-expanded={
                    menuOpen
                }
            >

                <span className="profile-trigger-avatar">

                    {
                        loading
                            ? (
                                <FaUser />
                            )
                            : (
                                getInitial() ||
                                <FaUser />
                            )
                    }

                </span>


                <span className="profile-trigger-details">

                    <strong>

                        {
                            loading
                                ? "Loading..."
                                : (
                                    profile?.username ||
                                    "Profile"
                                )
                        }

                    </strong>

                    {
                        profile?.role && (

                            <small>
                                {
                                    formatRole(
                                        profile.role
                                    )
                                }
                            </small>
                        )
                    }

                </span>


                <FaChevronDown
                    className={
                        menuOpen
                            ? (
                                "profile-menu-chevron " +
                                "open"
                            )
                            : "profile-menu-chevron"
                    }
                />

            </button>


            {
                menuOpen && (

                    <div className="profile-dropdown">

                        {
                            loading
                                ? (

                                    <div className="profile-dropdown-loading">

                                        Loading profile...

                                    </div>

                                )
                                : error
                                    ? (

                                        <div className="profile-dropdown-error">

                                            {error}

                                        </div>

                                    )
                                    : (

                                        <>

                                            <div className="profile-dropdown-header">

                                                <div className="profile-dropdown-avatar">

                                                    {
                                                        getInitial() ||
                                                        <FaUser />
                                                    }

                                                </div>


                                                <div>

                                                    <strong>
                                                        {
                                                            profile?.username
                                                        }
                                                    </strong>

                                                    <span>
                                                        {
                                                            formatRole(
                                                                profile?.role
                                                            )
                                                        }
                                                    </span>

                                                </div>

                                            </div>


                                            <div className="profile-dropdown-info">

                                                <div>

                                                    <FaEnvelope />

                                                    <span>
                                                        {
                                                            profile?.email
                                                        }
                                                    </span>

                                                </div>


                                                <div>

                                                    <FaIdBadge />

                                                    <span>
                                                        {
                                                            formatRole(
                                                                profile?.role
                                                            )
                                                        }
                                                    </span>

                                                </div>

                                            </div>


                                            <button
                                                type="button"
                                                className="view-profile-button"
                                                onClick={
                                                    handleViewProfile
                                                }
                                            >

                                                <FaUserCircle />

                                                <span>
                                                    My Profile
                                                </span>

                                            </button>

                                        </>
                                    )
                        }

                    </div>
                )
            }

        </div>
    );
}


export default ProfileMenu;