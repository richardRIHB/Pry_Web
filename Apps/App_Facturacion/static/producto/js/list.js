var tblProducto;
var modal_title;
var imag;
var iva;

function get_data() {
    tblProducto = $('#data').DataTable({
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
            {"data": "descripcion"},
            {"data": "precio"},
            {"data": "marca.nombre"},
            {"data": "nombre"},
            {"data": "stock"},
            {"data": "estado"},
            {"data": "imagen"},
            {"data": "nombre"},
        ],
        columnDefs: [
            {
                targets: [1],
                render: function (data, type, row) {
                    return '<a href="/App_Facturacion/producto/show/' + row.id + '/">' + row.nombre + '</a>';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" title="Editar Producto" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> ';
                    if (row.estado === true) {
                        buttons += '<a href="#" rel="delete" title="Eliminar Producto" class="btn btn-danger btn-xs btn-flat btnDelete"><i class="fas fa-trash-alt"></i></a> ';
                    }
                    return buttons
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + row.imagen + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;" >';
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
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
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    resul = parseFloat(data).toFixed();
                    return resul;
                }
            },
            {
                targets: [-5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return row.bloque.nombre + row.seccion.nombre + row.posicion.nombre ;
                }
            },
            {
                targets: [-7],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + data;
                }
            },
            {
                targets: [-8],
                render: function (data, type, row) {
                    html = data.substr(0, 25);
                    return html
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
};

function formatRepo_marca(repo) {
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
        '<div class="col-lg-12 text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.nombre + '<br>' +
        '<b>Estado:</b> ' + html +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

function formatRepo_ubicacion(repo) {
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
        '<div class="col-lg-12 text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.nombre + '<br>' +
        html +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function () {
    modal_title = $('.modal-title');
    get_data();
    $("input[name='precio_bruto']").TouchSpin({
        min:0,
        max: 500,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '$USD'
    })
    $("input[name='stock']").TouchSpin({
        min:0,
        max: 10000,
        step: 0.0001,
        decimals: 4,
        boostat: 5,
        maxboostedstep: 10,
        postfix: 'Uds'
    })
    $("input[name='stock_minimo']").TouchSpin({
        min:0,
        max: 10000,
        step: 1,
        decimals: 0,
        boostat: 5,
        maxboostedstep: 10,
        postfix: 'Uds'
    })
    $("input[name='porcentaje_ganancia']").TouchSpin({
        min:0,
        max: 200,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    })
    //Limpiar el modal al dar click en cerrar
    $('.cerrarModal').on('click', function () {
        limpiarFormModal();
    });

    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de un Producto');
        limpiarFormModal();
        $("#id_estado").attr('checked','True');
        $('input[name="porcentaje_ganancia"]').val(50);
        $('input[name="precio"]').val('0.00');
        $('input[name="precio_bruto"]').val('0.00');
        $('input[name="iva"]').val(iva);
        $('#myModalProducto').modal('show');
    });

    $('#data tbody')
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html('Edicion de un producto');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblProducto.cell($(this).closest('td, li')).index();
            var data = tblProducto.row(tr.row).data();
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="nombre"]').val(data.nombre);
            $('textarea[name="descripcion"]').val(data.descripcion);
            $('input[name="precio"]').val(data.precio);
            $('input[name="iva"]').val(iva);
            // Establecer el valor, o creando una nueva opción si es necesario
            if ($('select[name="marca"]').find("option[value='" + data.marca.id + "']").length) {
                $('select[name="marca"]').val(data.marca.id).trigger('change');
            } else {
                var newOption = new Option(data.marca.nombre, data.marca.id, true, true);
                $('select[name="marca"]').append(newOption).trigger('change');
            }
            if ($('select[name="bloque"]').find("option[value='" + data.bloque.id + "']").length) {
                $('select[name="bloque"]').val(data.bloque.id).trigger('change');
            } else {
                var newOption = new Option(data.bloque.nombre, data.bloque.id, true, true);
                $('select[name="bloque"]').append(newOption).trigger('change');
            }
            if ($('select[name="seccion"]').find("option[value='" + data.seccion.id + "']").length) {
                $('select[name="seccion"]').val(data.seccion.id).trigger('change');
            } else {
                var newOption = new Option(data.seccion.nombre, data.seccion.id, true, true);
                $('select[name="seccion"]').append(newOption).trigger('change');
            }
            if ($('select[name="posicion"]').find("option[value='" + data.posicion.id + "']").length) {
                $('select[name="posicion"]').val(data.posicion.id).trigger('change');
            } else {
                var newOption = new Option(data.posicion.nombre, data.posicion.id, true, true);
                $('select[name="posicion"]').append(newOption).trigger('change');
            }
            $('input[name="porcentaje_ganancia"]').val(data.porcentaje_ganancia);
            $('input[name="stock"]').val(data.stock);
            $('input[name="stock_minimo"]').val(data.stock_minimo);
            $('input[name="precio_bruto"]').val(data.precio_bruto);
            var iv = parseFloat($('input[name="iva"]').val());
            iv += 1;
            var precio_iva = parseFloat(data.precio_bruto * iv).toFixed(2);
            var utilidad = parseFloat(data.precio - precio_iva).toFixed(2);
            $('input[name="utilidad"]').val(utilidad);
            $('input[name="precio_iva"]').val(precio_iva);
            if (data.estado === true){
                $("#id_estado").attr('checked','True');
            }else {
                 $('#id_estado').removeAttr('checked','False');
            }
            imag = data.imagen
            mostarElemetosFormModal(data.imagen);
            $('#myModalProducto').modal('show');
        })
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblProducto.cell($(this).closest('td, li')).index();
            var data = tblProducto.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el registro Nº'+' <span  class="badge badge-success" > '+ data.id + '</span>' +'?', parameters, function () {
                limpiarFormModal();
                tblProducto.ajax.reload();
            });
        })

    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        var estado_val = document.getElementById('id_estado').checked;
        parameters.append('estado_valor', estado_val);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#myModalProducto').modal('hide');
            limpiarFormModal();
            tblProducto.ajax.reload();
        });
    });

    //Busqueda de marca con ajax
    $('select[name="marca"]').select2({
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
                    action: 'search_marca'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Buscar marca',
        minimumInputLength: 1,
        templateResult: formatRepo_marca,
    });

    $('select[name="bloque"]').select2({
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
                    action: 'search_bloque'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Buscar..',
        minimumInputLength: 1,
        templateResult: formatRepo_ubicacion,
    });

    $('select[name="seccion"]').select2({
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
                    action: 'search_seccion'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Buscar..',
        minimumInputLength: 1,
        templateResult: formatRepo_ubicacion,
    });

    $('select[name="posicion"]').select2({
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
                    action: 'search_posicion'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Buscar..',
        minimumInputLength: 1,
        templateResult: formatRepo_ubicacion,
    });

});
//acciones secundarias para activar otras acciones
$(document).ready(function () {
    $(document).on("click", "#btn_id", function () {
        $("#id_imagen").click();
    })
})

function validarInputFile() {
    var archivoInput = document.getElementById('id_imagen');
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
    var elementoMarca = document.querySelector("#select2-id_marca-container");
    var elementoBloque = document.querySelector("#select2-id_bloque-container");
    var elementoSeccion = document.querySelector("#select2-id_seccion-container");
    var elementoPosicion = document.querySelector("#select2-id_posicion-container");
    elementoMarca.innerHTML = '<span class="select2-selection__rendered" id="select2-id_marca-container" role="textbox" aria-readonly="true" title=""><span class="select2-selection__placeholder">Buscar marca</span></span>'
    elementoBloque.innerHTML = '<span class="select2-selection__rendered" id="select2-id_bloque-container" role="textbox" aria-readonly="true" title=""><span class="select2-selection__placeholder">Buscar..</span></span>'
    elementoSeccion.innerHTML = '<span class="select2-selection__rendered" id="select2-id_seccion-container" role="textbox" aria-readonly="true" title=""><span class="select2-selection__placeholder">Buscar..</span></span>'
    elementoPosicion.innerHTML = '<span class="select2-selection__rendered" id="select2-id_posicion-container" role="textbox" aria-readonly="true" title=""><span class="select2-selection__placeholder">Buscar..</span></span>'
    document.getElementById('visorArchivo').innerHTML =
        '<div> </div>';
}

//funcion para mostrar los datos del select
function mostarElemetosFormModal(ima) {
    //agg informacion
    document.getElementById('visorArchivo').innerHTML =
        '<img src="' + ima + '" alt="Mi imagen" id="miImagen" width="70%" height="200" border=50px>'
}

//funcion para calcular el pvp del precio ingresado por teclado
function calcularPVP() {
    var precio_b = parseFloat($('input[name="precio_bruto"]').val());
    var porcentaje_g = parseFloat($('input[name="porcentaje_ganancia"]').val());
    $('input[name="iva"]').val(iva);
    var iv = parseFloat($('input[name="iva"]').val());
    var pvp = 0;
    var utilidad = 0;
    var precio_iva = 0;
    if (precio_b && porcentaje_g >= 0){
        porcentaje_g =(porcentaje_g /100)+1;
        iv += 1;
        precio_iva = parseFloat(precio_b * iv).toFixed(2);
        pvp = parseFloat(precio_iva * porcentaje_g).toFixed(2);
        utilidad = parseFloat(pvp - precio_iva).toFixed(2);

    } else{
        pvp = parseFloat(pvp).toFixed(2);
        utilidad = parseFloat(utilidad).toFixed(2);
        precio_iva = parseFloat(precio_iva).toFixed(2);
    }
    $('input[name="precio"]').val(pvp);
    $('input[name="utilidad"]').val(utilidad);
    $('input[name="precio_iva"]').val(precio_iva);
}
