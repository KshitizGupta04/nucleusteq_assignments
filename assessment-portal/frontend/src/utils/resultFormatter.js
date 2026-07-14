export const formatPercentage = (
    percentage
) => {

    const numericPercentage = Number(
        percentage
    );

    if (
        Number.isNaN(
            numericPercentage
        )
    ) {

        return "0.00";
    }

    return numericPercentage.toFixed(
        2
    );
};


export const formatScore = (
    score
) => {

    const numericScore = Number(
        score
    );

    if (
        Number.isNaN(
            numericScore
        )
    ) {

        return "0";
    }

    return Number.isInteger(
        numericScore
    )
        ? numericScore
        : numericScore.toFixed(2);
};


export const formatNumber = (
    value
) => {

    const numericValue = Number(
        value
    );

    if (
        Number.isNaN(
            numericValue
        )
    ) {

        return "0";
    }

    return Number.isInteger(
        numericValue
    )
        ? numericValue
        : numericValue.toFixed(2);
};