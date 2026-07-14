import {
    FaCheckCircle,
    FaExclamationCircle,
    FaTimes
} from "react-icons/fa";


function Toast({
    toast,
    onClose
}) {

    if (!toast) {

        return null;
    }


    const isSuccess = (
        toast.type === "success"
    );


    return (

        <div
            className={
                `toast toast-${toast.type}`
            }
            role="alert"
        >

            <span className="toast-icon">

                {
                    isSuccess
                        ? <FaCheckCircle />
                        : <FaExclamationCircle />
                }

            </span>


            <span className="toast-message">

                {toast.message}

            </span>


            <button
                type="button"
                className="toast-close-button"
                onClick={onClose}
                aria-label="Close notification"
            >
                <FaTimes />
            </button>

        </div>
    );
}


export default Toast;