var tblGestion;
var modal_title;
var imag;

function get_data() {
    tblGestion = $('#data').DataTable({
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
            {"data": "inventario.id"},
            {"data": "inventario.producto.nombre"},
            {"data": "fecha"},
            {"data": "precio"},
            {"data": "cantidad"},
            {"data": "total"},
            {"data": "tipo_gestion"},
            {"data": "estado"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [0],
                render: function (data, type, row) {
                    return data;
                }
            },
            {
                targets: [1],
                orderable: false,
                render: function (data, type, row) {
                    return data +' '+ row.inventario.producto.marca.nombre +' '+ row.inventario.medida;
                }
            },
            {
                targets: [2],
                class: 'text-center',
                render: function (data, type, row) {
                    return data;
                }
            },
            {
                targets: [3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$'+data;
                }
            },
            {
                targets: [4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<span  class="badge badge-dark sorting" >' + data + ' </span>';
                }
            },
            {
                targets: [5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$'+data;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="ver" title="Ver Producto" class="btn btn-warning btn-xs btnEdit"><i class="fas fa-eye"></i></a> ';
                    if (row.estado === true) {
                        buttons += '<a href="#" rel="delete" title="Eliminar Producto" class="btn btn-danger btn-xs btnDelete"><i class="fas fa-trash-alt"></i></a> ';
                    }
                    return buttons
                }
            },
            {
                targets: [-2],
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
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var estado = 'De salida'
                    var html = '<span  class="badge badge-warning sorting" >'+ '<i class="fa fa-fw fa-minus-square"></i>' + estado + ' </span>'
                    if (data === true) {
                        estado = 'De entrada'
                        html = '<span  class="badge badge-success sorting" >'+ '<i class="fa fa-fw fa-plus-square"></i>' + estado + ' </span>'
                    }
                    return html
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
};

function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }
    var estado = 'Bloqueado'
    var html = '<span  class="badge badge-warning" >' + estado + '</span>'
    if (repo.estado === true) {
        estado = 'Activo'
        html = '<span  class="badge badge-success" >' + estado + '</span>'
    }
    pvp_bruto_iva = parseFloat(repo.producto.precio_bruto) * (parseFloat(repo.producto.iva) + 1);
    if (repo.tipo_conversion) {
        pvp_bruto_iva = parseFloat(pvp_bruto_iva) * parseFloat(repo.equivalencia);
    } else {
        pvp_bruto_iva = parseFloat(pvp_bruto_iva) / parseFloat(repo.equivalencia);
    }
    stock_r = parseInt(repo.producto.stock)
    cant_real = stock_r / repo.conversion_stock
    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.producto.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        repo.producto.nombre +' '+ repo.producto.marca.nombre +' '+ repo.medida + '<br>' +
        '<b>Precio:</b> <span class="badge badge-warning">$' + parseFloat(pvp_bruto_iva).toFixed(3) + '</span>' +
        '<b>Stock:</b> <span class="badge bg-dark">' + parseInt(cant_real) + '</span>' + ' ' +
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

    $("input[name='cantidad']").TouchSpin({
        min:1,
        max: 10000,
        step: 1,
        decimals: 0,
        boostat: 5,
        maxboostedstep: 10,
        postfix: 'Und'
    })
    //Limpiar el modal al dar click en cerrar
    $('.cerrarModal').on('click', function () {
        $('form')[0].reset();
        limpiarFormModal();
    });

    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de un Registro');
        $('input[name="cantidad"]').trigger("touchspin.updatesettings", {max: 10000});
        $('input[name="cantidad"]').trigger("touchspin.updatesettings", {min: 1});
        $('form')[0].reset();
        $('select[name="tipo_problema"]').val('1').trigger('change');
        $('select[name="tipo_gestion"]').val('True').trigger('change');
        limpiarFormModal();
        var elemento = document.querySelector(".text_producto");
        elemento.innerHTML = ''
        $("#id_estado").attr('checked','True');
        var footer = document.querySelector("#id_footer_m");
        footer.innerHTML = '<button type="submit" class="btn btn-primary btn-flat btn-block ">' +
                            '<i class="fas fa-save"></i>Guardar' +
                            '</button>'
        //Activador de los input
        $(".select2").prop("disabled", false);
        $("#id_cantidad").attr('readonly',false);
        $("#id_descripcion").attr('readonly',false);
        $("#id_tipo_gestion").prop('disabled',false);
        $("#id_tipo_problema").prop('disabled',false);
        $("#id_estado").attr('disabled',true);
        $('#myModalGestion').modal('show');
    });

    $('select[name="inventario"]').on('change', function () {
        var res = $(this).val();
        if (res === ''){
            $('input[name="precio"]').val('0.00');
            var elemento = document.querySelector(".text_producto");
            elemento.innerHTML = ''
        }
        calcularPVP();
    });

    $('#data tbody')
        .on('click', 'a[rel="ver"]', function () {
            modal_title.find('span').html('Detalle del registro');
            modal_title.find('i').removeClass().addClass('fas fa-eye');
            var tr = tblGestion.cell($(this).closest('td, li')).index();
            var data = tblGestion.row(tr.row).data();
            $('input[name="action"]').val('ver');
            $('input[name="id"]').val(data.id);
            $('input[name="cantidad"]').trigger("touchspin.updatesettings", {max: data.cantidad});
            $('input[name="cantidad"]').trigger("touchspin.updatesettings", {min: data.cantidad});
            // Establecer el valor, o creando una nueva opción si es necesario
            if ($('select[name="inventario"]').find("option[value='" + data.inventario.id + "']").length) {
                $('select[name="inventario"]').val(data.inventario.id).trigger('change');
            } else {
                var newOption = new Option(data.inventario.nombre, data.inventario.id, true, true);
                $('select[name="inventario"]').append(newOption).trigger('change');
            }
            if ( String(data.tipo_gestion) === 'true') {
                $('select[name="tipo_gestion"]').val('True').trigger('change');
            }else{
                $('select[name="tipo_gestion"]').val('False').trigger('change');
            }
            if ( data.tipo_problema === 1) {
                $('select[name="tipo_problema"]').val(1).trigger('change');
            }else if(data.tipo_problema === 2){
                $('select[name="tipo_problema"]').val(2).trigger('change');
            }else{
                $('select[name="tipo_problema"]').val(3).trigger('change');
            }
            $('textarea[name="descripcion"]').val(data.descripcion);
            $('input[name="precio"]').val(data.precio);
            $('input[name="cantidad"]').val(data.cantidad);
            $('input[name="total"]').val(data.total);

            if (data.estado === true){
                $("#id_estado").attr('checked','True');
            }else {
                 $('#id_estado').removeAttr('checked','False');
            }
            var elemento = document.querySelector(".text_producto");
            var footer = document.querySelector("#id_footer_m");
            footer.innerHTML = ''
            stock_r = parseInt(data.inventario.producto.stock)
            cant_real = stock_r / data.inventario.conversion_stock
            elemento.innerHTML = '<i class="fas fa-info-circle text_producto">'+'Descripcion: ' +  data.inventario.producto.nombre +' '+ data.inventario.producto.marca.nombre +' '+ data.inventario.medida +
                ' '+ '<span class="badge badge-dark">'+parseInt(cant_real)+'</span>'+'</i>'
            //bloqueo de los input
            $(".select2").prop("disabled", 'True');
            $("#id_cantidad").attr('readonly','True');
            $("#id_descripcion").attr('readonly','True');
            $("#id_tipo_gestion").prop('disabled','True');
            $("#id_tipo_problema").prop('disabled','True');
            $("#id_estado").attr('disabled','True');
            $('#myModalGestion').modal('show');
        })
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblGestion.cell($(this).closest('td, li')).index();
            var data = tblGestion.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el registro Nº '+'<span  class="badge badge-success" > '+ data.inventario.producto.id +'</span>'+ '<span  class="badge badge-primary" style="text-transform: uppercase;" > '+ data.inventario.producto.nombre+' '+ data.inventario.producto.marca.nombre +' '+ data.inventario.medida +'</span>' +'?', parameters, function () {
                $('form')[0].reset();
                tblGestion.ajax.reload();
            });
        })

    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        var estado_val = document.getElementById('id_estado').checked;
        parameters.append('estado_valor', estado_val);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#myModalGestion').modal('hide');
            $('form')[0].reset();
            limpiarFormModal();
            tblGestion.ajax.reload();
        });
    });

    //Busqueda de producto con ajax
    $('select[name="inventario"]').select2({
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
                    action: 'search_inventario'
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
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        pvp_bruto_iva = parseFloat(data.producto.precio_bruto) * (parseFloat(data.producto.iva) + 1);
        if (data.tipo_conversion) {
            pvp_bruto_iva = parseFloat(pvp_bruto_iva) * parseFloat(data.equivalencia);
        } else {
            pvp_bruto_iva = parseFloat(pvp_bruto_iva) / parseFloat(data.equivalencia);
        }
        $('input[name="precio"]').val(parseFloat(pvp_bruto_iva).toFixed(3));
        var elemento = document.querySelector(".text_producto");
        stock_r = parseInt(data.producto.stock)
        cant_real = stock_r / data.conversion_stock
        elemento.innerHTML = '<i class="fas fa-info-circle text_producto">'+'Descripcion: ' +  data.producto.nombre +' '+ data.producto.marca.nombre +' '+ data.medida +
            ' '+ '<span class="badge badge-dark">'+parseInt(cant_real)+'</span>'+'</i>'
        calcularPVP();
    });
});

//funcion para limpiar el formulario del modal
function limpiarFormModal() {
    var elementoProducto = document.querySelector("#select2-id_inventario-container");
    elementoProducto.innerHTML = '<span class="select2-selection__rendered" id="select2-id_inventario-container" role="textbox" aria-readonly="true" title=""><span class="select2-selection__placeholder">Buscar producto</span></span>'
}

//funcion para calcular
function calcularPVP() {

    var precio = parseFloat($('input[name="precio"]').val());
    var cantidad = $('input[name="cantidad"]').val();
    if (isNaN(cantidad) || cantidad===''){
        cantidad = 1
        $('input[name="cantidad"]').val(1);
    }
    total = parseFloat(precio * cantidad).toFixed(2);

    $('input[name="total"]').val(total);
}
