const validarEmailAdmin = email => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

const validarPasswordAdmin = password => {
    if(password.length === 6){
        return true;
    }else{
    return false;
    }
}

