function direccionFieldCallback(data) {
    console.log("Callback de dirección:", data);
}

function autocompleteQuery(data) {
    console.log("Usuario escribiendo:", data.direccion);
    direccionFieldCallback(data);
}

function initAutocomplete() {
    var direccionField = document.querySelector('.autocomplete');
    
    if (!direccionField) {
        console.error("Elemento con clase 'autocomplete' no encontrado en el documento.");
        return;
    }

    var autocomplete = new google.maps.places.Autocomplete(direccionField, {
        types: ['geocode'],
        fields: ['formatted_address'],
        origin: 'https://maps.googleapis.com/maps/api/place',
        strictBounds: false,
        componentRestrictions: { country: 'cl' },
        sessionToken: new google.maps.places.AutocompleteSessionToken(),
    });

    autocomplete.addListener('place_changed', function () {
        var place = autocomplete.getPlace();
        
        // Verifica si la dirección contiene "Puente Alto"
        var containsPuenteAlto = place.formatted_address.includes("Puente Alto");

        // Lógica para ajustar el total de la compra
        var cargoExtra = containsPuenteAlto ? 0 : 3000;
        console.log("Cargo extra:", cargoExtra);
    });
}


    var autocomplete = new google.maps.places.Autocomplete(direccionField, {
        types: ['geocode'],
        fields: ['formatted_address'],
        origin: 'https://maps.googleapis.com/maps/api/place',
        strictBounds: false,
        componentRestrictions: { country: 'cl' },
        sessionToken: new google.maps.places.AutocompleteSessionToken(),
    });

    autocomplete.addListener('place_changed', function () {
        var place = autocomplete.getPlace();
        console.log(place);
    });


try {
    initAutocomplete();
} catch (error) {
    console.error("Error loading Google Maps:", error);
}

function searchNearbyPlaces() {
    // Código de búsqueda cercana si es necesario
}
