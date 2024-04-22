const validarNombre = nombre => {
    if(nombre.length >= 4 && nombre.length <= 12) {
        return true;
    }else {
        return false;
    }
}

const validarEmail = email => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

const validarPassword1 = password1 => {
    return password1.length >= 6; 
}

