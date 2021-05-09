var tblGaleria;
var modal_title;
var imag;

function get_data() {
    tblGaleria = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "nombre"},
            {"data": "producto.nombre"},
            {"data": "producto.marca.nombre"},
            {"data": "estado"},
            {"data": "ruta"},
            {"data": "nombre"},
        ],
        columnDefs: [
            {
                targets: [1],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<a href="/App_Facturacion/galeria/show/' + row.id + '/">' + row.nombre + '</a>';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" title="Editar Galeria" class="btn btn-warning btn-xs btnEdit"><i class="fas fa-edit"></i></a> ';
                    if (row.estado === true) {
                        buttons += '<a href="#" rel="delete" title="Eliminar Galeria" class="btn btn-danger btn-xs btnDelete"><i class="fas fa-trash-alt"></i></a> ';
                    }
                    return buttons
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + row.ruta + '" class="img-fluid d-block mx-auto" style="width: 50px; height: 50px;">';
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                render: function (data, type, row) {
                    var estado = 'Bloqueado'
                    var html = '<span  class="badge badge-warning sorting" >' + estado + ' </span>'
                    if (row.estado === true) {
                        estado = 'Activo'
                        html = '<span  class="badge badge-success sorting" >' + estado + ' </span>'
                    }
                    return html
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
};

function formatRepoProducto(repo) {
    if (repo.loading) {
        return repo.text;
    }
    var estado = 'Bloqueado'
    var html = '<span  class="badge badge-warning" >' + estado + '</span>'
    if (repo.estado === true) {
        estado = 'Activo'
        html = '<span  class="badge badge-success" >' + estado + '</span>'
    }
    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-2">' +
        '<img src="' + repo.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-10 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.nombre + '<br>' +
        '<b>Marca:</b> ' + repo.marca.nombre + '<br>' +
        '<b>Estado:</b> ' + html +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function () {
    modal_title = $('.modal-title');
    get_data();
    //Limpiar el modal al dar click en cerrar
    $('.cerrarModal').on('click', function () {
        limpiarFormModal();
        $('#myModalGaleria').modal('hide');
    });
    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de una Galería');
        limpiarFormModal();
        $("#id_estado").attr('checked','True');
        $('#myModalGaleria').modal('show');
    });

    $('#data tbody')
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html('Edicion de una Galería');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblGaleria.cell($(this).closest('td, li')).index();
            var data = tblGaleria.row(tr.row).data();
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="nombre"]').val(data.nombre);
            // Establecer el valor, o creando una nueva opción si es necesario
            if ($('select[name="producto"]').find("option[value='" + data.producto.id + "']").length) {
                $('select[name="producto"]').val(data.producto.id).trigger('change');
            } else {
                var newOption = new Option(data.producto.nombre, data.producto.id, true, true);
                $('select[name="producto"]').append(newOption).trigger('change');
            }
            imag = data.ruta
            mostarElemetosFormModal(data.ruta);
            if (data.estado === true){
                $("#id_estado").attr('checked','True');
            }else {
                 $('#id_estado').removeAttr('checked','False');
            }
            $('#myModalGaleria').modal('show');
        })
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblGaleria.cell($(this).closest('td, li')).index();
            var data = tblGaleria.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el registro Nº'+' <span  class="badge badge-success" > '+ data.id + '</span>' +'?', parameters, function () {
                limpiarFormModal();
                $('#myModalGaleria').modal('hide');
                tblGaleria.ajax.reload();
            });
        });

    $('form').on('submit', function (e) {
        //validar el input file de imagen
        var archivoAccion;
        var archivoInput;
        archivoAccion = document.getElementById('id_accion');
        if (archivoAccion.value == "add"){
            archivoInput = document.getElementById('id_ruta');
            if (archivoInput.value == ""){
                Swal.fire({
                    title: 'Advertencia !',
                    text: 'Seleccione una imagen.',
                    icon: 'warning'
                });
                return false;
            } else {
                e.preventDefault();
                var parameters = new FormData(this);
                submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                    limpiarFormModal();
                    $('#myModalGaleria').modal('hide');
                    tblGaleria.ajax.reload();
                });
            }
        } else {
            e.preventDefault();
            var parameters2 = new FormData(this);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters2, function () {
                limpiarFormModal();
                $('#myModalGaleria').modal('hide');
                tblGaleria.ajax.reload();
            });
        }
    });

    //Busqueda de producto con ajax
    $('select[name="producto"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_producto'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Buscar producto',
        minimumInputLength: 1,
        templateResult: formatRepoProducto,
    });
});

//acciones secundarias para activar otras acciones
$(document).ready(function () {
    $(document).on("click", "#btn_id", function () {
        $("#id_ruta").click();
    })

})

function validarInputFile() {
    var archivoInput = document.getElementById('id_ruta');
    var accion = $('input[name="action"]').val()
    var archivoRuta = archivoInput.value;
    var extencionesPermitidas = /(.png|.PNG|.jpg|.jpeg)$/i;

    if (!extencionesPermitidas.exec(archivoRuta)) {
        Swal.fire({
            title: 'Error!',
            text: 'Asegúrate de haber seleccionado una imagen.',
            icon: 'error'
        });
        archivoInput.value = '';
        if (accion === 'edit'){
            document.getElementById('visorArchivo').innerHTML =
                '<img src="' + imag + '" alt="Mi imagen" id="miImagen" width="70%" height="200" border=50px>'
        }else{
            document.getElementById('visorArchivo').innerHTML =
                '<div> </div>';
        }
        return false;
    } else {
        if (archivoInput.files && archivoInput.files[0]) {
            var visor = new FileReader();
            visor.onload = function (e) {
                document.getElementById('visorArchivo').innerHTML =
                    '<img src="' + e.target.result + '" alt="Mi imagen" id="miImagen" width="70%" height="200" border=50px>';
            };
            visor.readAsDataURL(archivoInput.files[0]);
        }
    }
}

//funcion para limpiar el formulario del modal
function limpiarFormModal() {
    $('form')[0].reset();
    //limpiar el contenido de seleccion
    var elementoProducto = document.querySelector("#select2-id_producto-container");
    elementoProducto.innerHTML = '<span class="select2-selection__rendered" id="select2-id_producto-container" role="textbox" aria-readonly="true" title=""><span class="select2-selection__placeholder">Buscar producto</span></span>'
    document.getElementById('visorArchivo').innerHTML =
        '<div> </div>';
}

//funcion para mostrar la imagen
function mostarElemetosFormModal(ruta) {
    document.getElementById('visorArchivo').innerHTML =
        '<img src="' + ruta + '" alt="Mi imagen" id="miImagen" width="70%" height="200" border=50px>'
}