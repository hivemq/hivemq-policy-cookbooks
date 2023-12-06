function maskString(inputString) {
    if (inputString.length <= 2) {
        return inputString;
    }

    const firstChar = inputString.charAt(0);
    const lastChar = inputString.charAt(inputString.length - 1);
    
    const maskedChars = '*'.repeat(inputString.length - 2);
    
    const maskedString = firstChar + maskedChars + lastChar;

    return maskedString;
}

function extractYearFromDate(dateString) {
    const year = dateString.split('-')[0];
    return `${year}-01-01`;
}

function transform(publish, context) {
    publish.payload = {
    	"id": publish.payload.id,
    	"name": publish.payload.name,
        "surname": maskString(publish.payload.surname),
        "dateOfBirth": extractYearFromDate(publish.payload.dateOfBirth),
        "address": {
            "street": "[REDACTED]",
            "city": publish.payload.address.city,
            "zipCode": "[REDACTED]",
            "country": publish.payload.address.country
        }
    }

    return publish;
}