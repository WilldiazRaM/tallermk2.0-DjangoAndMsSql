const validarRut = rut => {
    if (rut.length >= 9) {
        return true
    }else{       
        return false
    }
    };

                       
    const validarNombre = nombre => {
    if (nombre.length >=4 && nombre.length <=15 ) {
        return true
    }else {
        return false
    }
    };

    

    const validaraPaterno = aPaterno => {
        if (aPaterno.length >=4 && aPaterno.length <=16 ) {
            return true
        }else{
            return false
        }
    };

    const validarApMaterno = apMaterno => {
        if (apMaterno.length >=4 && apMaterno.length <= 16) {
            return true
        }else {
            return false
        }
    };

    const validarCelular = celular => {
        if (!isNaN(celular) && celular.toString().length === 9){
            return true;                       
        }else{
        return false
    }
    
    };
    
    const validarTextArea = textoMotivo => {
        if (textoMotivo.length >= 10 && textoMotivo.length <= 250) {
            return true
        }else {
            return false
        }
    };

    (function () {
        'use strict'
    
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.querySelectorAll('.needs-validation')
    
        // Loop over them and prevent submission
        Array.prototype.slice.call(forms)
          .forEach(function (form) {
            form.addEventListener('submit', function (event) {
              if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
              }
    
              form.classList.add('was-validated')
            }, false)
          })
      })() 