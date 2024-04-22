const validarEmailMecanico = email => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}


const validarPasswordMecanico = password => {
    if(password.length === 6){
        return true;
    }else{
    return false;
    }
}

