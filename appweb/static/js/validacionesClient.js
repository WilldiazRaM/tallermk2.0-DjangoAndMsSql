const validarEmail = email => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}


const validarPassword = password => {
    if(password.length === 6){
        return true;
    }else{
    return false;
    }
}

