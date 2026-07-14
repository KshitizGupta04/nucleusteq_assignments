import {
    useEffect,
    useState
} from "react";

import {
    FaEdit,
    FaPlus,
    FaTrash
} from "react-icons/fa";

import Pagination from "../../components/common/Pagination";
import Toast from "../../components/common/Toast";

import usePagination from "../../hooks/usePagination";
import useToast from "../../hooks/useToast";

import {
    createCategory,
    deleteCategory,
    getCategories,
    updateCategory
} from "../../services/adminService";


const ITEMS_PER_PAGE = 5;

const EMPTY_FORM = {
    name: "",
    description: ""
};


function CategoryManagement() {

    const [
        categories,
        setCategories
    ] = useState([]);

    const [
        formData,
        setFormData
    ] = useState(EMPTY_FORM);

    const [
        errors,
        setErrors
    ] = useState({});

    const [
        touched,
        setTouched
    ] = useState({});

    const [
        editingCategoryId,
        setEditingCategoryId
    ] = useState(null);

    const [
        loading,
        setLoading
    ] = useState(true);

    const [
        submitting,
        setSubmitting
    ] = useState(false);

    const [
        deletingCategoryId,
        setDeletingCategoryId
    ] = useState(null);


    const {
        toast,
        showSuccess,
        showError,
        clearToast
    } = useToast();


    const {
        currentPage,
        totalPages,
        paginatedItems: paginatedCategories,
        goToPreviousPage,
        goToNextPage
    } = usePagination(
        categories,
        ITEMS_PER_PAGE
    );


    const validateField = (
        name,
        value
    ) => {

        const trimmedValue = value.trim();

        const rules = {
            name: {
                required: "Category name is required.",
                minLength: 3,
                minMessage: (
                    "Category name must be at least 3 characters."
                ),
                maxLength: 100,
                maxMessage: (
                    "Category name cannot exceed 100 characters."
                )
            },
            description: {
                required: "Description is required.",
                minLength: 5,
                minMessage: (
                    "Description must be at least 5 characters."
                ),
                maxLength: 255,
                maxMessage: (
                    "Description cannot exceed 255 characters."
                )
            }
        };

        const rule = rules[name];

        if (!rule) {

            return "";
        }

        if (!trimmedValue) {

            return rule.required;
        }

        if (
            trimmedValue.length <
            rule.minLength
        ) {

            return rule.minMessage;
        }

        if (
            trimmedValue.length >
            rule.maxLength
        ) {

            return rule.maxMessage;
        }

        return "";
    };


    const validateForm = () => {

        return Object.keys(
            EMPTY_FORM
        ).reduce(
            (
                validationErrors,
                fieldName
            ) => {

                validationErrors[
                    fieldName
                ] = validateField(
                    fieldName,
                    formData[fieldName]
                );

                return validationErrors;
            },
            {}
        );
    };


    const fetchCategories = async () => {

        setLoading(true);

        try {

            const response = (
                await getCategories()
            );

            setCategories(
                Array.isArray(response)
                    ? response
                    : []
            );

        } catch (error) {

            showError(
                error.message
            );

        } finally {

            setLoading(false);
        }
    };


    useEffect(
        () => {

            fetchCategories();

        },
        []
    );


    const handleChange = (
        event
    ) => {

        const {
            name,
            value
        } = event.target;

        setFormData(
            previous => ({
                ...previous,
                [name]: value
            })
        );

        setTouched(
            previous => ({
                ...previous,
                [name]: true
            })
        );

        setErrors(
            previous => ({
                ...previous,
                [name]: validateField(
                    name,
                    value
                )
            })
        );
    };


    const handleBlur = (
        event
    ) => {

        const {
            name,
            value
        } = event.target;

        setTouched(
            previous => ({
                ...previous,
                [name]: true
            })
        );

        setErrors(
            previous => ({
                ...previous,
                [name]: validateField(
                    name,
                    value
                )
            })
        );
    };


    const resetForm = () => {

        setFormData(
            EMPTY_FORM
        );

        setErrors({});

        setTouched({});

        setEditingCategoryId(
            null
        );
    };


    const handleSubmit = async (
        event
    ) => {

        event.preventDefault();

        const validationErrors = (
            validateForm()
        );

        setErrors(
            validationErrors
        );

        setTouched({
            name: true,
            description: true
        });

        const hasErrors = Object.values(
            validationErrors
        ).some(Boolean);

        if (hasErrors) {

            return;
        }

        setSubmitting(true);

        const name = (
            formData.name.trim()
        );

        const description = (
            formData.description.trim()
        );

        try {

            if (editingCategoryId) {

                await updateCategory(
                    editingCategoryId,
                    name,
                    description
                );

                showSuccess(
                    "Category updated successfully."
                );

            } else {

                await createCategory(
                    name,
                    description
                );

                showSuccess(
                    "Category created successfully."
                );
            }

            resetForm();

            await fetchCategories();

        } catch (error) {

            showError(
                error.message
            );

        } finally {

            setSubmitting(false);
        }
    };


    const handleEdit = (
        category
    ) => {

        setEditingCategoryId(
            category.id
        );

        setFormData({
            name: category.name,
            description: category.description
        });

        setErrors({});

        setTouched({});

        clearToast();

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    };


    const handleCancelEdit = () => {

        resetForm();

        clearToast();
    };


    const handleDelete = async (
        category
    ) => {

        const confirmed = window.confirm(
            `Are you sure you want to delete "${category.name}"?`
        );

        if (!confirmed) {

            return;
        }

        setDeletingCategoryId(
            category.id
        );

        try {

            await deleteCategory(
                category.id
            );

            if (
                editingCategoryId ===
                category.id
            ) {

                resetForm();
            }

            showSuccess(
                "Category deleted successfully."
            );

            await fetchCategories();

        } catch (error) {

            showError(
                error.message
            );

        } finally {

            setDeletingCategoryId(
                null
            );
        }
    };


    const getInputClassName = (
        fieldName
    ) => {

        if (!touched[fieldName]) {

            return "form-input";
        }

        if (errors[fieldName]) {

            return "form-input input-error";
        }

        if (formData[fieldName]) {

            return "form-input input-valid";
        }

        return "form-input";
    };


    const isFormValid = () => {

        return Object.values(
            validateForm()
        ).every(
            error => !error
        );
    };


    return (

        <div className="category-management">

            <Toast
                toast={toast}
                onClose={clearToast}
            />


            <section className="management-form-card">

                <div className="section-heading">

                    <div>

                        <h2>
                            {
                                editingCategoryId
                                    ? "Update Category"
                                    : "Create Category"
                            }
                        </h2>

                        <p>
                            {
                                editingCategoryId
                                    ? (
                                        "Update the selected " +
                                        "category details."
                                    )
                                    : (
                                        "Add a new assessment " +
                                        "category."
                                    )
                            }
                        </p>

                    </div>

                </div>


                <form
                    onSubmit={handleSubmit}
                    noValidate
                >

                    <div className="form-group">

                        <label
                            htmlFor="category-name"
                        >
                            Category Name
                        </label>

                        <input
                            id="category-name"
                            name="name"
                            type="text"
                            value={formData.name}
                            onChange={handleChange}
                            onBlur={handleBlur}
                            className={
                                getInputClassName(
                                    "name"
                                )
                            }
                            placeholder="Enter category name"
                            maxLength={100}
                        />

                        {
                            touched.name &&
                            errors.name && (

                                <p className="field-error">
                                    {errors.name}
                                </p>
                            )
                        }

                    </div>


                    <div className="form-group">

                        <label
                            htmlFor="category-description"
                        >
                            Description
                        </label>

                        <textarea
                            id="category-description"
                            name="description"
                            value={
                                formData.description
                            }
                            onChange={handleChange}
                            onBlur={handleBlur}
                            className={
                                getInputClassName(
                                    "description"
                                )
                            }
                            placeholder={
                                "Enter category description"
                            }
                            rows={4}
                            maxLength={255}
                        />

                        <div className="field-footer">

                            {
                                touched.description &&
                                errors.description ? (

                                    <p className="field-error">
                                        {
                                            errors.description
                                        }
                                    </p>

                                ) : (

                                    <span />

                                )
                            }

                            <span className="character-count">
                                {
                                    formData
                                        .description
                                        .length
                                }/255
                            </span>

                        </div>

                    </div>


                    <div className="form-actions">

                        <button
                            type="submit"
                            className="primary-button"
                            disabled={
                                submitting ||
                                !isFormValid()
                            }
                        >

                            {
                                submitting ? (

                                    editingCategoryId
                                        ? "Updating..."
                                        : "Creating..."

                                ) : (

                                    <>

                                        {
                                            editingCategoryId
                                                ? <FaEdit />
                                                : <FaPlus />
                                        }

                                        <span>
                                            {
                                                editingCategoryId
                                                    ? "Update Category"
                                                    : "Create Category"
                                            }
                                        </span>

                                    </>
                                )
                            }

                        </button>


                        {
                            editingCategoryId && (

                                <button
                                    type="button"
                                    className="secondary-button"
                                    onClick={
                                        handleCancelEdit
                                    }
                                    disabled={submitting}
                                >
                                    Cancel
                                </button>
                            )
                        }

                    </div>

                </form>

            </section>


            <section className="management-list-card">

                <div className="section-heading">

                    <div>

                        <h2>
                            All Categories
                        </h2>

                        <p>
                            {categories.length} {
                                categories.length === 1
                                    ? "category"
                                    : "categories"
                            } available
                        </p>

                    </div>

                </div>


                {
                    loading ? (

                        <div className="loading-state">
                            Loading categories...
                        </div>

                    ) : categories.length === 0 ? (

                        <div className="empty-state">

                            <h3>
                                No categories found
                            </h3>

                            <p>
                                Create your first category
                                using the form above.
                            </p>

                        </div>

                    ) : (

                        <>

                            <div
                                className={
                                    "management-table-wrapper"
                                }
                            >

                                <table
                                    className="management-table"
                                >

                                    <thead>

                                        <tr>

                                            <th>
                                                Name
                                            </th>

                                            <th>
                                                Description
                                            </th>

                                            <th>
                                                Actions
                                            </th>

                                        </tr>

                                    </thead>


                                    <tbody>

                                        {
                                            paginatedCategories.map(
                                                category => (

                                                    <tr
                                                        key={
                                                            category.id
                                                        }
                                                    >

                                                        <td>

                                                            <strong>
                                                                {
                                                                    category.name
                                                                }
                                                            </strong>

                                                        </td>

                                                        <td>
                                                            {
                                                                category.description
                                                            }
                                                        </td>

                                                        <td>

                                                            <div
                                                                className={
                                                                    "table-actions"
                                                                }
                                                            >

                                                                <button
                                                                    type="button"
                                                                    className={
                                                                        "icon-button " +
                                                                        "edit-button"
                                                                    }
                                                                    onClick={
                                                                        () =>
                                                                            handleEdit(
                                                                                category
                                                                            )
                                                                    }
                                                                    aria-label={
                                                                        `Edit ${category.name}`
                                                                    }
                                                                >
                                                                    <FaEdit />
                                                                </button>


                                                                <button
                                                                    type="button"
                                                                    className={
                                                                        "icon-button " +
                                                                        "delete-button"
                                                                    }
                                                                    onClick={
                                                                        () =>
                                                                            handleDelete(
                                                                                category
                                                                            )
                                                                    }
                                                                    disabled={
                                                                        deletingCategoryId ===
                                                                        category.id
                                                                    }
                                                                    aria-label={
                                                                        `Delete ${category.name}`
                                                                    }
                                                                >

                                                                    {
                                                                        deletingCategoryId ===
                                                                        category.id
                                                                            ? "..."
                                                                            : <FaTrash />
                                                                    }

                                                                </button>

                                                            </div>

                                                        </td>

                                                    </tr>
                                                )
                                            )
                                        }

                                    </tbody>

                                </table>

                            </div>


                            <Pagination
                                currentPage={currentPage}
                                totalPages={totalPages}
                                onPrevious={
                                    goToPreviousPage
                                }
                                onNext={
                                    goToNextPage
                                }
                            />

                        </>

                    )
                }

            </section>

        </div>
    );
}


export default CategoryManagement;