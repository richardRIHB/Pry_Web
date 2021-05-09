var imag;
var imag2;
function get_data() {
    $.ajax({
        type:"POST",
        dataType:"json",
        url: window.location.pathname,
        data : { action : 'search_empresa' },
        success: function (response) {
            if (response.length !== 0){
                $('input[name="action"]').val('edit');
                $('input[name="id"]').val(response['0'].id);
                $('input[name="nombre"]').val(response['0'].nombre);
                $('input[name="ruc"]').val(response['0'].ruc);
                $('input[name="telefono"]').val(response['0'].telefono);
                $('input[name="correo"]').val(response['0'].correo);
                $('input[name="ciudad"]').val(response['0'].ciudad);
                $('input[name="direccion"]').val(response['0'].direccion);
                $('input[name="sitio_web"]').val(response['0'].sitio_web);
                $('input[name="iva"]').val(response['0'].iva);
                imag = response['0'].imagen
                imag2 = response['0'].logo_login
                mostarElemetosFormModal(response['0'].imagen, response['0'].logo_login)
            }else{
                imag = '/static/img/logo.png'
                imag2 = '/static/img/logo.png'
                mostarElemetosFormModal(imag,imag2)
            }
        },
        error: function (error) {
            console.log(error)
        }
    });
}

$(function () {
    get_data()
    $("input[name='iva']").TouchSpin({
        min:0.01,
        max: 0.15,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function () {
        if (isNaN(parseFloat($(this).val()))) {
            $(this).val(0.01);
        }
    })

    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/App_Facturacion/empresa/';
        });
    });

});
//acciones secundarias para activar otras acciones
$(document).ready(function () {
    $(document).on("click", "#btn_id", function () {
        $("#id_imagen").click();
    })
    $(document).on("click", "#btn_id_logo", function () {
        $("#id_logo_login").click();
    })
})

function validarInputFile() {
    var archivoInput = document.getElementById('id_imagen');
    var accion = $('input[name="action"]').val()
    var archivoRuta = archivoInput.value;
    var extencionesPermitidas = /(.png|.PNG|.jpg|.JPEG)$/i;

    if (!extencionesPermitidas.exec(archivoRuta)) {
        Swal.fire({
            title: 'Error!',
            text: 'Asegúrate de haber seleccionado una imagen.',
            icon: 'error'
        });
        archivoInput.value = '';
        document.getElementById('visorArchivo').innerHTML =
            '<img src="' + imag + '" alt="Mi imagen" id="miImagen" width="100%" height="164" border=50px>'

        return false;
    } else {
        if (archivoInput.files && archivoInput.files[0]) {
            var visor = new FileReader();
            visor.onload = function (e) {
                document.getElementById('visorArchivo').innerHTML =
                    '<img src="' + e.target.result + '" alt="Mi imagen" id="miImagen" width="100%" height="164" border=50px>'
            };
            visor.readAsDataURL(archivoInput.files[0]);
        }
    }
}

function validarInputFile_logo() {
    var archivoInput = document.getElementById('id_logo_login');
    var archivoRuta = archivoInput.value;
    var extencionesPermitidas = /(.png|.PNG|.jpg|.JPEG)$/i;

    if (!extencionesPermitidas.exec(archivoRuta)) {
        Swal.fire({
            title: 'Error!',
            text: 'Asegúrate de haber seleccionado una imagen.',
            icon: 'error'
        });
        archivoInput.value = '';
        document.getElementById('visorArchivo_logo').innerHTML =
            '<img src="' + imag2 + '" alt="Mi imagen" id="miImagen2" width="100%" height="250" border=50px>'

        return false;
    } else {
        if (archivoInput.files && archivoInput.files[0]) {
            var visor = new FileReader();
            visor.onload = function (e) {
                document.getElementById('visorArchivo_logo').innerHTML =
                    '<img src="' + e.target.result + '" alt="Mi imagen" id="miImagen2" width="100%" height="250" border=50px>'
            };
            visor.readAsDataURL(archivoInput.files[0]);
        }
    }
}

//funcion para mostrar los datos del select
function mostarElemetosFormModal(ima, ima2) {
    //agg informacion
    document.getElementById('visorArchivo').innerHTML =
        '<img src="' + ima + '" alt="Mi imagen" id="miImagen" width="100%" height="164" border=50px>'
    document.getElementById('visorArchivo_logo').innerHTML =
        '<img src="' + ima2 + '" alt="Mi imagen" id="miImagen2" width="100%" height="250" border=50px>'
}
