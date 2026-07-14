import {
    useCallback,
    useEffect,
    useRef,
    useState
} from "react";


const DEFAULT_DURATION = 3000;


function useToast() {

    const [
        toast,
        setToast
    ] = useState(null);

    const timeoutRef = useRef(null);


    const clearToast = useCallback(
        () => {

            if (timeoutRef.current) {

                clearTimeout(
                    timeoutRef.current
                );

                timeoutRef.current = null;
            }

            setToast(null);
        },
        []
    );


    const showToast = useCallback(
        (
            message,
            type = "success",
            duration = DEFAULT_DURATION
        ) => {

            if (timeoutRef.current) {

                clearTimeout(
                    timeoutRef.current
                );
            }

            setToast({
                message,
                type
            });

            timeoutRef.current = setTimeout(
                () => {

                    setToast(null);

                    timeoutRef.current = null;
                },
                duration
            );
        },
        []
    );


    const showSuccess = useCallback(
        (
            message,
            duration
        ) => {

            showToast(
                message,
                "success",
                duration
            );
        },
        [
            showToast
        ]
    );


    const showError = useCallback(
        (
            message,
            duration
        ) => {

            showToast(
                message,
                "error",
                duration
            );
        },
        [
            showToast
        ]
    );


    useEffect(
        () => {

            return () => {

                if (timeoutRef.current) {

                    clearTimeout(
                        timeoutRef.current
                    );
                }
            };
        },
        []
    );


    return {
        toast,
        showSuccess,
        showError,
        clearToast
    };
}


export default useToast;