import {
    useEffect,
    useState
} from "react";

import {
    FaCalendarAlt,
    FaCheckCircle,
    FaClipboardList,
    FaEnvelope,
    FaIdBadge,
    FaTimesCircle,
    FaUser,
    FaUserCircle
} from "react-icons/fa";

import {
    getMyProfile,
} from "../services/authService";

import {
    getMyResults
} from "../services/studentService";


function MyProfile() {

    const [
        profile,
        setProfile
    ] = useState(null);


    const [
        results,
        setResults
    ] = useState([]);


    const [
        loading,
        setLoading
    ] = useState(true);


    const [
        error,
        setError
    ] = useState("");


    useEffect(
        () => {

            const loadProfile = async () => {

                try {

                    setLoading(true);

                    setError("");


                    const profileData = (
                        await getMyProfile()
                    );


                    setProfile(
                        profileData
                    );


                    if (
                        profileData?.role ===
                        "student"
                    ) {

                        const resultData = (
                            await getMyResults()
                        );


                        setResults(
                            Array.isArray(
                                resultData
                            )
                                ? resultData
                                : []
                        );
                    }

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


    const formatRole = (
        role
    ) => {

        if (!role) {

            return "Not available";
        }


        return (
            role.charAt(0).toUpperCase() +
            role.slice(1)
        );
    };


    const formatDate = (
        dateValue
    ) => {

        if (!dateValue) {

            return "Not available";
        }


        const date = new Date(
            dateValue
        );


        if (
            Number.isNaN(
                date.getTime()
            )
        ) {

            return "Not available";
        }


        return date.toLocaleDateString(
            "en-IN",
            {
                day: "numeric",
                month: "long",
                year: "numeric"
            }
        );
    };


    const getInitial = () => {

        if (
            !profile?.username
        ) {

            return (
                <FaUser />
            );
        }


        return profile.username
            .charAt(0)
            .toUpperCase();
    };


    const totalAttempts = (
        results.length
    );


    const passedAttempts = (
        results.filter(
            result =>
                result.status === "pass"
        ).length
    );


    const failedAttempts = (
        results.filter(
            result =>
                result.status !== "pass"
        ).length
    );


    if (loading) {

        return (

            <div className="management-loading">

                Loading profile...

            </div>
        );
    }


    if (error) {

        return (

            <div className="error-message">

                {error}

            </div>
        );
    }


    if (!profile) {

        return (

            <div className="empty-state">

                <FaUserCircle
                    className="empty-state-icon"
                />

                <h3>
                    Profile unavailable
                </h3>

                <p>
                    Your profile information could
                    not be loaded.
                </p>

            </div>
        );
    }


    return (

        <div className="my-profile-page">

            <div className="profile-card">

                <div className="profile-card-header">

                    <div className="profile-large-avatar">

                        {getInitial()}

                    </div>


                    <div className="profile-card-identity">

                        <h2>
                            {profile.username}
                        </h2>

                        <span className="profile-role-badge">

                            {
                                formatRole(
                                    profile.role
                                )
                            }

                        </span>

                    </div>

                </div>


                <div className="profile-details-section">

                    <h3>
                        Account Information
                    </h3>


                    <div className="profile-details-grid">

                        <div className="profile-detail-item">

                            <div className="profile-detail-icon">

                                <FaUser />

                            </div>


                            <div>

                                <span className="profile-detail-label">
                                    Username
                                </span>

                                <strong>
                                    {profile.username}
                                </strong>

                            </div>

                        </div>


                        <div className="profile-detail-item">

                            <div className="profile-detail-icon">

                                <FaEnvelope />

                            </div>


                            <div>

                                <span className="profile-detail-label">
                                    Email Address
                                </span>

                                <strong>
                                    {profile.email}
                                </strong>

                            </div>

                        </div>


                        <div className="profile-detail-item">

                            <div className="profile-detail-icon">

                                <FaIdBadge />

                            </div>


                            <div>

                                <span className="profile-detail-label">
                                    Role
                                </span>

                                <strong>

                                    {
                                        formatRole(
                                            profile.role
                                        )
                                    }

                                </strong>

                            </div>

                        </div>


                        <div className="profile-detail-item">

                            <div className="profile-detail-icon">

                                <FaCalendarAlt />

                            </div>


                            <div>

                                <span className="profile-detail-label">
                                    Member Since
                                </span>

                                <strong>

                                    {
                                        formatDate(
                                            profile.created_at
                                        )
                                    }

                                </strong>

                            </div>

                        </div>

                    </div>

                </div>


                {
                    profile.role === "student" && (

                        <div className="profile-activity-section">

                            <h3>
                                Assessment Activity
                            </h3>


                            <div className="profile-activity-grid">

                                <div
                                    className={
                                        "profile-activity-card " +
                                        "total"
                                    }
                                >

                                    <div className="profile-activity-icon">

                                        <FaClipboardList />

                                    </div>


                                    <div>

                                        <strong>
                                            {totalAttempts}
                                        </strong>

                                        <span>
                                            Total Attempts
                                        </span>

                                    </div>

                                </div>


                                <div
                                    className={
                                        "profile-activity-card " +
                                        "passed"
                                    }
                                >

                                    <div className="profile-activity-icon">

                                        <FaCheckCircle />

                                    </div>


                                    <div>

                                        <strong>
                                            {passedAttempts}
                                        </strong>

                                        <span>
                                            Passed
                                        </span>

                                    </div>

                                </div>


                                <div
                                    className={
                                        "profile-activity-card " +
                                        "failed"
                                    }
                                >

                                    <div className="profile-activity-icon">

                                        <FaTimesCircle />

                                    </div>


                                    <div>

                                        <strong>
                                            {failedAttempts}
                                        </strong>

                                        <span>
                                            Failed
                                        </span>

                                    </div>

                                </div>

                            </div>

                        </div>
                    )
                }

            </div>

        </div>
    );
}


export default MyProfile;