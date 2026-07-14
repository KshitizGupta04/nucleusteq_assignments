import {
    useEffect,
    useMemo,
    useState
} from "react";

import {
    FaArrowLeft,
    FaCheckCircle,
    FaChevronRight,
    FaClipboardCheck,
    FaEye,
    FaSearch,
    FaTimesCircle,
    FaUser,
    FaUsers
} from "react-icons/fa";

import {
    getAdminResults,
    getQuizzes,
    getResultBreakdown
} from "../../services/adminService";


function AdminResults() {

    const [
        results,
        setResults
    ] = useState([]);

    const [
        quizzes,
        setQuizzes
    ] = useState([]);

    const [
        selectedStudent,
        setSelectedStudent
    ] = useState(null);

    const [
        selectedResult,
        setSelectedResult
    ] = useState(null);

    const [
        breakdown,
        setBreakdown
    ] = useState([]);

    const [
        searchTerm,
        setSearchTerm
    ] = useState("");

    const [
        loading,
        setLoading
    ] = useState(true);

    const [
        breakdownLoading,
        setBreakdownLoading
    ] = useState(false);

    const [
        error,
        setError
    ] = useState("");

    const [
        breakdownError,
        setBreakdownError
    ] = useState("");


    useEffect(
        () => {

            const loadAdminResults = async () => {

                setLoading(true);

                setError("");

                try {

                    const [
                        resultsData,
                        quizzesData
                    ] = await Promise.all([
                        getAdminResults(),
                        getQuizzes()
                    ]);


                    setResults(
                        Array.isArray(
                            resultsData
                        )
                            ? resultsData
                            : []
                    );


                    setQuizzes(
                        Array.isArray(
                            quizzesData
                        )
                            ? quizzesData
                            : []
                    );

                } catch (err) {

                    setError(
                        err.message ||
                        "Failed to load student results."
                    );

                } finally {

                    setLoading(false);
                }
            };


            loadAdminResults();

        },
        []
    );


    const quizTitleMap = useMemo(
        () => {

            return quizzes.reduce(
                (
                    map,
                    quiz
                ) => {

                    const quizId = (
                        quiz.id ||
                        quiz._id
                    );


                    if (quizId) {

                        map[quizId] = (
                            quiz.title ||
                            "Untitled Quiz"
                        );
                    }


                    return map;
                },
                {}
            );

        },
        [
            quizzes
        ]
    );


    const groupedStudents = useMemo(
        () => {

            const studentMap = {};


            results.forEach(
                result => {

                    const studentId = (
                        result.student_id ||
                        "Unknown Student"
                    );


                    if (!studentMap[studentId]) {

                        studentMap[studentId] = {
                            studentId,
                            results: [],
                            totalResults: 0,
                            passedResults: 0,
                            failedResults: 0
                        };
                    }


                    studentMap[
                        studentId
                    ].results.push(
                        result
                    );


                    studentMap[
                        studentId
                    ].totalResults += 1;


                    if (
                        String(
                            result.status
                        ).toLowerCase() ===
                        "pass"
                    ) {

                        studentMap[
                            studentId
                        ].passedResults += 1;

                    } else {

                        studentMap[
                            studentId
                        ].failedResults += 1;
                    }
                }
            );


            return Object.values(
                studentMap
            ).sort(
                (
                    firstStudent,
                    secondStudent
                ) => {

                    return (
                        firstStudent.studentId.localeCompare(
                            secondStudent.studentId
                        )
                    );
                }
            );

        },
        [
            results
        ]
    );


    const filteredStudents = useMemo(
        () => {

            const normalizedSearch = (
                searchTerm
                    .trim()
                    .toLowerCase()
            );


            if (!normalizedSearch) {

                return groupedStudents;
            }


            return groupedStudents.filter(
                student => {

                    return student.studentId
                        .toLowerCase()
                        .includes(
                            normalizedSearch
                        );
                }
            );

        },
        [
            groupedStudents,
            searchTerm
        ]
    );


    const selectedStudentData = useMemo(
        () => {

            if (!selectedStudent) {

                return null;
            }


            return groupedStudents.find(
                student =>
                    student.studentId ===
                    selectedStudent
            ) || null;

        },
        [
            groupedStudents,
            selectedStudent
        ]
    );


    const getQuizTitle = (
        quizId
    ) => {

        return (
            quizTitleMap[quizId] ||
            "Quiz"
        );
    };


    const handleStudentSelect = (
        studentId
    ) => {

        setSelectedStudent(
            studentId
        );

        setSelectedResult(
            null
        );

        setBreakdown([]);

        setSearchTerm("");
    };


    const handleBackToStudents = () => {

        setSelectedStudent(
            null
        );

        setSelectedResult(
            null
        );

        setBreakdown([]);

        setBreakdownError("");
    };


    const handleViewBreakdown = async (
        result
    ) => {

        setSelectedResult(
            result
        );

        setBreakdown([]);

        setBreakdownError("");

        setBreakdownLoading(
            true
        );


        try {

            const data = (
                await getResultBreakdown(
                    result.result_id
                )
            );


            setBreakdown(
                Array.isArray(data)
                    ? data
                    : []
            );

        } catch (err) {

            setBreakdownError(
                err.message ||
                "Failed to load result breakdown."
            );

        } finally {

            setBreakdownLoading(
                false
            );
        }
    };


    const handleBackToStudentResults = () => {

        setSelectedResult(
            null
        );

        setBreakdown([]);

        setBreakdownError("");
    };


    if (loading) {

        return (

            <div className="admin-results-loading">

                <FaClipboardCheck />

                <p>
                    Loading student results...
                </p>

            </div>
        );
    }


    if (error) {

        return (

            <div className="admin-results-error">

                {error}

            </div>
        );
    }


    if (
        selectedStudentData &&
        selectedResult
    ) {

        const isPassed = (
            String(
                selectedResult.status
            ).toLowerCase() ===
            "pass"
        );


        return (

            <div className="admin-results-page">

                <button
                    type="button"
                    className="back-to-students-button"
                    onClick={
                        handleBackToStudentResults
                    }
                >

                    <FaArrowLeft />

                    <span>
                        Back to Student Results
                    </span>

                </button>


                <section className="admin-breakdown-header">

                    <div>

                        <span className="admin-results-label">
                            RESULT BREAKDOWN
                        </span>

                        <h2>
                            {
                                selectedStudentData
                                    .studentId
                            }'s Assessment
                        </h2>

                        <p>
                            {
                                getQuizTitle(
                                    selectedResult.quiz_id
                                )
                            }
                            {" · Attempt "}
                            {
                                selectedResult
                                    .attempt_number
                            }
                        </p>

                    </div>


                    <span
                        className={
                            isPassed
                                ? (
                                    "admin-result-status " +
                                    "passed"
                                )
                                : (
                                    "admin-result-status " +
                                    "failed"
                                )
                        }
                    >

                        {
                            isPassed
                                ? (
                                    <FaCheckCircle />
                                )
                                : (
                                    <FaTimesCircle />
                                )
                        }

                        {
                            isPassed
                                ? "Pass"
                                : "Fail"
                        }

                    </span>

                </section>


                <section className="admin-breakdown-summary">

                    <div>

                        <span>
                            Score
                        </span>

                        <strong>

                            {
                                Number(
                                    selectedResult
                                        .score_obtained ||
                                    0
                                ).toFixed(
                                    1
                                )
                            }

                            {" / "}

                            {
                                Number(
                                    selectedResult
                                        .total_marks ||
                                    0
                                ).toFixed(
                                    0
                                )
                            }

                        </strong>

                    </div>


                    <div>

                        <span>
                            Percentage
                        </span>

                        <strong>

                            {
                                Number(
                                    selectedResult
                                        .percentage ||
                                    0
                                ).toFixed(
                                    1
                                )
                            }%

                        </strong>

                    </div>


                    <div>

                        <span>
                            Questions
                        </span>

                        <strong>
                            {breakdown.length}
                        </strong>

                    </div>

                </section>


                {
                    breakdownLoading
                        ? (

                            <div className="admin-results-loading">

                                <FaClipboardCheck />

                                <p>
                                    Loading result breakdown...
                                </p>

                            </div>

                        )
                        : breakdownError
                            ? (

                                <div className="admin-results-error">

                                    {breakdownError}

                                </div>

                            )
                            : breakdown.length === 0
                                ? (

                                    <div className="admin-results-empty">

                                        <FaClipboardCheck />

                                        <h3>
                                            No breakdown available
                                        </h3>

                                        <p>
                                            No question details were
                                            found for this result.
                                        </p>

                                    </div>

                                )
                                : (

                                    <section className="admin-breakdown-list">

                                        {
                                            breakdown.map(
                                                (
                                                    question,
                                                    index
                                                ) => {

                                                    return (

                                                        <article
                                                            key={
                                                                question.question_id ||
                                                                index
                                                            }
                                                            className={
                                                                question.is_correct
                                                                    ? (
                                                                        "admin-breakdown-question " +
                                                                        "correct"
                                                                    )
                                                                    : (
                                                                        "admin-breakdown-question " +
                                                                        "incorrect"
                                                                    )
                                                            }
                                                        >

                                                            <div className="admin-breakdown-question-header">

                                                                <span className="admin-question-number">

                                                                    Question {
                                                                        index + 1
                                                                    }

                                                                </span>


                                                                <span
                                                                    className={
                                                                        question.is_correct
                                                                            ? (
                                                                                "admin-question-status " +
                                                                                "correct"
                                                                            )
                                                                            : (
                                                                                "admin-question-status " +
                                                                                "incorrect"
                                                                            )
                                                                    }
                                                                >

                                                                    {
                                                                        question.is_correct
                                                                            ? (
                                                                                <FaCheckCircle />
                                                                            )
                                                                            : (
                                                                                <FaTimesCircle />
                                                                            )
                                                                    }

                                                                    {
                                                                        question.is_correct
                                                                            ? "Correct"
                                                                            : "Incorrect"
                                                                    }

                                                                </span>

                                                            </div>


                                                            <h3>
                                                                {
                                                                    question.question
                                                                }
                                                            </h3>


                                                            <div className="admin-answer-grid">

                                                                <div className="admin-answer-box selected">

                                                                    <span>
                                                                        Selected Answer
                                                                    </span>

                                                                    <strong>

                                                                        {
                                                                            question.selected_answer ??
                                                                            "Not answered"
                                                                        }

                                                                    </strong>

                                                                </div>


                                                                <div className="admin-answer-box correct">

                                                                    <span>
                                                                        Correct Answer
                                                                    </span>

                                                                    <strong>
                                                                        {
                                                                            question.correct_answer
                                                                        }
                                                                    </strong>

                                                                </div>

                                                            </div>


                                                            <div className="admin-question-marks">

                                                                <span>
                                                                    Marks Obtained
                                                                </span>

                                                                <strong>
                                                                    {
                                                                        Number(
                                                                            question.marks_obtained ||
                                                                            0
                                                                        ).toFixed(
                                                                            1
                                                                        )
                                                                    }
                                                                </strong>

                                                            </div>

                                                        </article>
                                                    );
                                                }
                                            )
                                        }

                                    </section>
                                )
                }

            </div>
        );
    }


    if (selectedStudentData) {

        return (

            <div className="admin-results-page">

                <button
                    type="button"
                    className="back-to-students-button"
                    onClick={
                        handleBackToStudents
                    }
                >

                    <FaArrowLeft />

                    <span>
                        Back to Students
                    </span>

                </button>


                <section className="student-results-header">

                    <div className="student-results-avatar">

                        <FaUser />

                    </div>


                    <div className="student-results-header-content">

                        <span className="student-results-label">
                            STUDENT PERFORMANCE
                        </span>

                        <h2>
                            {
                                selectedStudentData
                                    .studentId
                            }'s Results
                        </h2>

                        <p>
                            View complete assessment history
                            and performance details.
                        </p>

                    </div>

                </section>


                <section className="student-results-summary">

                    <div className="student-summary-card">

                        <span>
                            Total Results
                        </span>

                        <strong>
                            {
                                selectedStudentData
                                    .totalResults
                            }
                        </strong>

                    </div>


                    <div className="student-summary-card passed">

                        <span>
                            Passed
                        </span>

                        <strong>
                            {
                                selectedStudentData
                                    .passedResults
                            }
                        </strong>

                    </div>


                    <div className="student-summary-card failed">

                        <span>
                            Failed
                        </span>

                        <strong>
                            {
                                selectedStudentData
                                    .failedResults
                            }
                        </strong>

                    </div>

                </section>


                <section className="admin-student-result-grid">

                    {
                        selectedStudentData
                            .results
                            .map(
                                result => {

                                    const isPassed = (
                                        String(
                                            result.status
                                        ).toLowerCase() ===
                                        "pass"
                                    );


                                    return (

                                        <article
                                            key={
                                                result.result_id
                                            }
                                            className="admin-student-result-card"
                                        >

                                            <div className="admin-result-card-header">

                                                <div>

                                                    <span className="admin-result-attempt">

                                                        Attempt {
                                                            result.attempt_number
                                                        }

                                                    </span>


                                                    <h3>
                                                        {
                                                            getQuizTitle(
                                                                result.quiz_id
                                                            )
                                                        }
                                                    </h3>

                                                </div>


                                                <span
                                                    className={
                                                        isPassed
                                                            ? (
                                                                "admin-result-status " +
                                                                "passed"
                                                            )
                                                            : (
                                                                "admin-result-status " +
                                                                "failed"
                                                            )
                                                    }
                                                >

                                                    {
                                                        isPassed
                                                            ? (
                                                                <FaCheckCircle />
                                                            )
                                                            : (
                                                                <FaTimesCircle />
                                                            )
                                                    }

                                                    {
                                                        isPassed
                                                            ? "Pass"
                                                            : "Fail"
                                                    }

                                                </span>

                                            </div>


                                            <div className="admin-result-score-section">

                                                <div>

                                                    <span>
                                                        Score
                                                    </span>

                                                    <strong>

                                                        {
                                                            Number(
                                                                result.score_obtained ||
                                                                0
                                                            ).toFixed(
                                                                1
                                                            )
                                                        }

                                                        {" / "}

                                                        {
                                                            Number(
                                                                result.total_marks ||
                                                                0
                                                            ).toFixed(
                                                                0
                                                            )
                                                        }

                                                    </strong>

                                                </div>


                                                <div>

                                                    <span>
                                                        Percentage
                                                    </span>

                                                    <strong>

                                                        {
                                                            Number(
                                                                result.percentage ||
                                                                0
                                                            ).toFixed(
                                                                1
                                                            )
                                                        }%

                                                    </strong>

                                                </div>

                                            </div>


                                            <button
                                                type="button"
                                                className="admin-view-breakdown-button"
                                                onClick={
                                                    () =>
                                                        handleViewBreakdown(
                                                            result
                                                        )
                                                }
                                            >

                                                <FaEye />

                                                <span>
                                                    View Breakdown
                                                </span>

                                            </button>

                                        </article>
                                    );
                                }
                            )
                    }

                </section>

            </div>
        );
    }


    return (

        <div className="admin-results-page">

            <section className="admin-results-header">

                <div>

                    <span className="admin-results-label">
                        STUDENT PERFORMANCE
                    </span>

                    <h2>
                        Student Results
                    </h2>

                    <p>
                        Select a student to view their
                        complete assessment history.
                    </p>

                </div>


                <div className="admin-results-total">

                    <FaUsers />

                    <div>

                        <strong>
                            {groupedStudents.length}
                        </strong>

                        <span>
                            Students
                        </span>

                    </div>

                </div>

            </section>


            <div className="admin-student-search">

                <FaSearch />

                <input
                    type="text"
                    value={searchTerm}
                    onChange={
                        event =>
                            setSearchTerm(
                                event.target.value
                            )
                    }
                    placeholder="Search students..."
                />

            </div>


            {
                groupedStudents.length === 0
                    ? (

                        <div className="admin-results-empty">

                            <FaClipboardCheck />

                            <h3>
                                No results available
                            </h3>

                            <p>
                                Student results will appear
                                here after quiz attempts are
                                submitted.
                            </p>

                        </div>

                    )
                    : filteredStudents.length === 0
                        ? (

                            <div className="admin-results-empty">

                                <FaSearch />

                                <h3>
                                    No student found
                                </h3>

                                <p>
                                    Try searching with a
                                    different student name.
                                </p>

                            </div>

                        )
                        : (

                            <section className="admin-student-grid">

                                {
                                    filteredStudents.map(
                                        student => {

                                            return (

                                                <button
                                                    key={
                                                        student.studentId
                                                    }
                                                    type="button"
                                                    className="admin-student-card"
                                                    onClick={
                                                        () =>
                                                            handleStudentSelect(
                                                                student.studentId
                                                            )
                                                    }
                                                >

                                                    <div className="admin-student-avatar">

                                                        <FaUser />

                                                    </div>


                                                    <div className="admin-student-info">

                                                        <h3>
                                                            {
                                                                student.studentId
                                                            }
                                                        </h3>

                                                        <p>
                                                            {
                                                                student.totalResults
                                                            } assessment {
                                                                student.totalResults === 1
                                                                    ? "result"
                                                                    : "results"
                                                            }
                                                        </p>


                                                        <div className="admin-student-stats">

                                                            <span className="passed">

                                                                {
                                                                    student.passedResults
                                                                } Passed

                                                            </span>


                                                            <span className="failed">

                                                                {
                                                                    student.failedResults
                                                                } Failed

                                                            </span>

                                                        </div>

                                                    </div>


                                                    <div className="admin-student-arrow">

                                                        <FaChevronRight />

                                                    </div>

                                                </button>
                                            );
                                        }
                                    )
                                }

                            </section>
                        )
            }

        </div>
    );
}


export default AdminResults;