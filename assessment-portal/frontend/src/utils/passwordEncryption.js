const PUBLIC_KEY_URL = "/public_key.pem";


const pemToArrayBuffer = (
    pem
) => {

    const base64 = pem
        .replace(
            "-----BEGIN PUBLIC KEY-----",
            ""
        )
        .replace(
            "-----END PUBLIC KEY-----",
            ""
        )
        .replace(
            /\s/g,
            ""
        );

    const binaryString = window.atob(
        base64
    );

    const bytes = new Uint8Array(
        binaryString.length
    );

    for (
        let index = 0;
        index < binaryString.length;
        index += 1
    ) {

        bytes[index] = (
            binaryString.charCodeAt(
                index
            )
        );
    }

    return bytes.buffer;
};


const arrayBufferToBase64 = (
    buffer
) => {

    const bytes = new Uint8Array(
        buffer
    );

    let binaryString = "";

    for (
        let index = 0;
        index < bytes.length;
        index += 1
    ) {

        binaryString += String.fromCharCode(
            bytes[index]
        );
    }

    return window.btoa(
        binaryString
    );
};


const loadPublicKey = async () => {

    const response = await fetch(
        PUBLIC_KEY_URL
    );

    if (!response.ok) {

        throw new Error(
            "Unable to load encryption key."
        );
    }

    const publicKeyPem = await response.text();

    const publicKeyBuffer = pemToArrayBuffer(
        publicKeyPem
    );

    return window.crypto.subtle.importKey(
        "spki",
        publicKeyBuffer,
        {
            name: "RSA-OAEP",
            hash: "SHA-256"
        },
        false,
        [
            "encrypt"
        ]
    );
};


export const encryptPassword = async (
    password
) => {

    const publicKey = await loadPublicKey();

    const encodedPassword = (
        new TextEncoder().encode(
            password
        )
    );

    const encryptedPassword = (
        await window.crypto.subtle.encrypt(
            {
                name: "RSA-OAEP"
            },
            publicKey,
            encodedPassword
        )
    );

    return arrayBufferToBase64(
        encryptedPassword
    );
};