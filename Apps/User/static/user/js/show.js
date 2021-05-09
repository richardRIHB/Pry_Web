//acciones secundarias para activar otras acciones
$(document).ready(function () {
    $(document).on("click", "#btn_id", function () {
        $("#id_imagen").click();
    })

})

function validarInputFile() {
    var archivoInput = document.getElementById('id_imagen');
    var archivoRuta = archivoInput.value;
    var extencionesPermitidas = /(.png|.PNG|.jpg|.jpeg)$/i;

    if (!extencionesPermitidas.exec(archivoRuta)) {
        Swal.fire({
            title: 'Error!',
            text: 'Asegúrate de haber seleccionado una imagen.',
            icon: 'error'
        });
        archivoInput.value = '';
        document.getElementById('visorArchivo').innerHTML =
            '<img src="' + imag + '" alt="Mi imagen" id="miImagen" width="95%" height="250" border=50px>';
        return false;
    } else {
        if (archivoInput.files && archivoInput.files[0]) {
            var visor = new FileReader();
            visor.onload = function (e) {
                document.getElementById('visorArchivo').innerHTML =
                    '<img src="' + e.target.result + '" alt="Mi imagen" id="miImagen" width="95%" height="250" border=50px>';
            };
            visor.readAsDataURL(archivoInput.files[0]);
        }
    }
}
