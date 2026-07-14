function Pagination({
    currentPage,
    totalPages,
    onPrevious,
    onNext
}) {

    if (
        totalPages <= 1
    ) {

        return null;
    }


    return (

        <div className="pagination">

            <button
                type="button"
                className="pagination-button"
                disabled={
                    currentPage === 1
                }
                onClick={
                    onPrevious
                }
            >
                Previous
            </button>


            <span className="pagination-info">

                Page {
                    currentPage
                } of {
                    totalPages
                }

            </span>


            <button
                type="button"
                className="pagination-button"
                disabled={
                    currentPage ===
                    totalPages
                }
                onClick={
                    onNext
                }
            >
                Next
            </button>

        </div>
    );
}


export default Pagination;