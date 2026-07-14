import {
    useCallback,
    useEffect,
    useMemo,
    useState
} from "react";


function usePagination(
    items = [],
    itemsPerPage = 5
) {

    const [
        currentPage,
        setCurrentPage
    ] = useState(1);


    const totalPages = Math.max(
        1,
        Math.ceil(
            items.length /
            itemsPerPage
        )
    );


    useEffect(
        () => {

            if (
                currentPage > totalPages
            ) {

                setCurrentPage(
                    totalPages
                );
            }

        },
        [
            currentPage,
            totalPages
        ]
    );


    const paginatedItems = useMemo(
        () => {

            const startIndex = (
                (currentPage - 1) *
                itemsPerPage
            );

            return items.slice(
                startIndex,
                startIndex +
                itemsPerPage
            );

        },
        [
            items,
            itemsPerPage,
            currentPage
        ]
    );


    const goToPreviousPage = useCallback(
        () => {

            setCurrentPage(
                previousPage => Math.max(
                    1,
                    previousPage - 1
                )
            );

        },
        []
    );


    const goToNextPage = useCallback(
        () => {

            setCurrentPage(
                previousPage => Math.min(
                    totalPages,
                    previousPage + 1
                )
            );

        },
        [
            totalPages
        ]
    );


    const goToPage = useCallback(
        (
            page
        ) => {

            const validPage = Math.min(
                Math.max(
                    1,
                    page
                ),
                totalPages
            );

            setCurrentPage(
                validPage
            );

        },
        [
            totalPages
        ]
    );


    const resetPage = useCallback(
        () => {

            setCurrentPage(
                1
            );

        },
        []
    );


    return {
        currentPage,
        totalPages,
        paginatedItems,
        goToPreviousPage,
        goToNextPage,
        goToPage,
        resetPage
    };
}


export default usePagination;