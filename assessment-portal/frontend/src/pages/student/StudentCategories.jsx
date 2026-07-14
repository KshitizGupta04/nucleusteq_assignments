import {
    useEffect,
    useState
} from "react";

import {
    FaBook,
    FaEye,
    FaFolderOpen
} from "react-icons/fa";

import {
    getCategories,
    getQuizzes
} from "../../services/studentService";


function StudentCategories({
    onViewQuizzes
}) {

    const [
        categories,
        setCategories
    ] = useState([]);

    const [
        quizzes,
        setQuizzes
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

            const loadData = async () => {

                try {

                    setLoading(true);

                    setError("");

                    const [
                        categoryData,
                        quizData
                    ] = await Promise.all([
                        getCategories(),
                        getQuizzes()
                    ]);

                    setCategories(
                        Array.isArray(
                            categoryData
                        )
                            ? categoryData
                            : []
                    );

                    setQuizzes(
                        Array.isArray(
                            quizData
                        )
                            ? quizData
                            : []
                    );

                } catch (err) {

                    setError(
                        err.message ||
                        "Failed to load categories."
                    );

                } finally {

                    setLoading(false);
                }
            };


            loadData();

        },
        []
    );


    const getQuizCount = (
        categoryId
    ) => {

        return quizzes.filter(
            quiz =>
                quiz.category_id ===
                categoryId
        ).length;
    };


    if (loading) {

        return (

            <div className="management-loading">

                Loading categories...

            </div>
        );
    }


    return (

        <div className="student-categories-page">

            {
                error && (

                    <div className="error-message">

                        {error}

                    </div>
                )
            }


            {
                categories.length === 0
                    ? (

                        <div className="empty-state">

                            <FaFolderOpen
                                className="empty-state-icon"
                            />

                            <h3>
                                No categories available
                            </h3>

                            <p>
                                There are currently no
                                assessment categories
                                available.
                            </p>

                        </div>
                    )
                    : (

                        <div className="student-category-grid">

                            {
                                categories.map(
                                    category => {

                                        const quizCount = (
                                            getQuizCount(
                                                category.id
                                            )
                                        );


                                        return (

                                            <article
                                                key={
                                                    category.id
                                                }
                                                className={
                                                    "student-category-card"
                                                }
                                            >

                                                <div
                                                    className={
                                                        "student-category-icon"
                                                    }
                                                >

                                                    <FaFolderOpen />

                                                </div>


                                                <div
                                                    className={
                                                        "student-category-content"
                                                    }
                                                >

                                                    <h3>

                                                        {
                                                            category.name
                                                        }

                                                    </h3>


                                                    <p>

                                                        {
                                                            category.description
                                                        }

                                                    </p>

                                                </div>


                                                <div
                                                    className={
                                                        "student-category-meta"
                                                    }
                                                >

                                                    <FaBook />

                                                    <span>

                                                        {
                                                            quizCount
                                                        }

                                                        {" "}

                                                        {
                                                            quizCount === 1
                                                                ? "Quiz"
                                                                : "Quizzes"
                                                        }

                                                    </span>

                                                </div>


                                                <button
                                                    type="button"
                                                    className={
                                                        "view-category-quizzes-button"
                                                    }
                                                    onClick={
                                                        () =>
                                                            onViewQuizzes(
                                                                category
                                                            )
                                                    }
                                                >

                                                    <FaEye />

                                                    <span>
                                                        View Quizzes
                                                    </span>

                                                </button>

                                            </article>
                                        );
                                    }
                                )
                            }

                        </div>
                    )
            }

        </div>
    );
}


export default StudentCategories;