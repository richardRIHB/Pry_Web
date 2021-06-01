var tblInventario;
var modal_title;
var imag;

function get_data() {
    tblInventario = $('#data').DataTable({
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
            {"data": "producto.nombre"},
            {"data": "medida"},
            {"data": "producto.stock"},
            {"data": "pvp_medida"},
            {"data": "porcentaje_conversion"},
            {"data": "estado"},
            {"data": "nombre"},
        ],
        columnDefs: [
            {
                targets: [0],
                render: function (data, type, row) {
                    return row.producto.id;
                }
            },
            {
                targets: [1],
                orderable: false,
                render: function (data, type, row) {
                    return '<a href="/App_Facturacion/producto/show/' + row.producto.id + '/">' + data + '-' + row.producto.marca.nombre + '-' + row.producto.descripcion.substr(0, 30) + '</a>';
                }
            },
            {
                targets: [2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return data;
                }
            },
            {
                targets: [3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    stock_r = parseInt(data)
                    cant_real = stock_r / row.conversion_stock
                    return '<span  class="badge badge-primary">' + parseInt(cant_real) + '</span>';
                }
            },
            {
                targets: [4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" title="Editar Producto" class="btn btn-warning btn-xs btnEdit"><i class="fas fa-edit"></i></a> ';
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
                    var html = '<span  class="badge badge-success sorting" title="GANANCIA"><i class="fas fa-arrow-up"></i></span>'
                    if (row.tipo_conversion === true) {
                        html = '<span  class="badge badge-danger sorting" title="DESCUENTO"><i class="fas fa-arrow-down"></i></span>'
                    }
                    if (data==='0.00'){
                        html = '<span  class="badge badge-dark sorting" ><i class="fas fa-minus"></i>'
                    }
                    return data + '% ' + html
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

    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        repo.nombre + ' ' + repo.descripcion.substr(0, 160) + '<br>' +
        '<b>Marca:</b> <span class="badge bg-dark">' + repo.marca.nombre + '</span>' + ' ' +
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

    $("input[name='equivalencia']").TouchSpin({
        min:0,
        max: 1000,
        step: 0.001,
        decimals: 3,
        boostat: 5,
        maxboostedstep: 10,
        postfix: 'Eqv'
    })
    $("input[name='porcentaje_conversion']").TouchSpin({
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
        $('form')[0].reset();
        limpiarFormModal();
    });

    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de un Producto de Inventario');
        $('form')[0].reset();
        $('select[name="tipo_conversion"]').val('True').trigger('change');
        limpiarFormModal();
        var elemento = document.querySelector(".text_producto");
        elemento.innerHTML = ''
        $("#id_estado").attr('checked','True');
        $('#myModalInventario').modal('show');
    });

    $('select[name="producto"]').on('change', function () {
        var res = $('select[name="producto"]').val();
        if (res === ''){
            $('input[name="pvp"]').val('0.00');
            $('input[name="conversion_stock"]').val('0.00');
            var elemento = document.querySelector(".text_producto");
            elemento.innerHTML = ''
        }
        calcularPVP();
    });

    $('select[name="tipo_conversion"]').on('change', function () {
        calcularPVP();
    });

    $('#data tbody')
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html('Edicion de un Producto de Inventario');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblInventario.cell($(this).closest('td, li')).index();
            var data = tblInventario.row(tr.row).data();
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            // Establecer el valor, o creando una nueva opción si es necesario
            if ($('select[name="producto"]').find("option[value='" + data.producto.id + "']").length) {
                $('select[name="producto"]').val(data.producto.id).trigger('change');
            } else {
                var newOption = new Option(data.producto.nombre, data.producto.id, true, true);
                $('select[name="producto"]').append(newOption).trigger('change');
            }
            if ( String(data.tipo_conversion) === 'true') {
                $('select[name="tipo_conversion"]').val('True').trigger('change');
            }else{
                $('select[name="tipo_conversion"]').val('False').trigger('change');
            }
            $('input[name="medida"]').val(data.medida);
            $('input[name="equivalencia"]').val(data.equivalencia);
            $('input[name="pvp"]').val(data.producto.precio);
            $('input[name="pvp_medida"]').val(data.pvp_medida);
            $('input[name="porcentaje_conversion"]').val(data.porcentaje_conversion);
            $('input[name="conversion_stock"]').val(data.conversion_stock);

            if (data.estado === true){
                $("#id_estado").attr('checked','True');
            }else {
                 $('#id_estado').removeAttr('checked','False');
            }
            stock_r = parseInt(data.producto.stock)
            cant_real = stock_r / data.conversion_stock
            var elemento = document.querySelector(".text_producto");
            elemento.innerHTML = '<i class="fas fa-info-circle text_producto">'+'Descripcion: ' +  data.producto.nombre +' '+ data.producto.marca.nombre +' '+ data.medida +
                ' '+ '<span class="badge badge-dark">'+parseInt(cant_real)+'</span>'+'</i>'
            //calcularPVP();
            $('#myModalInventario').modal('show');
        })
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblInventario.cell($(this).closest('td, li')).index();
            var data = tblInventario.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el registro Nº '+'<span  class="badge badge-success" > '+ data.producto.id +'</span>'+ '<span  class="badge badge-primary" style="text-transform: uppercase;" > '+ data.producto.nombre+' '+ data.producto.marca.nombre +' '+ data.medida +'</span>' +'?', parameters, function () {
                $('form')[0].reset();
                tblInventario.ajax.reload();
            });
        })
    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        var estado_val = document.getElementById('id_estado').checked;
        parameters.append('estado_valor', estado_val);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#myModalInventario').modal('hide');
            $('form')[0].reset();
            limpiarFormModal();
            tblInventario.ajax.reload();
        });
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
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        $('input[name="pvp"]').val(data.precio);
        var elemento = document.querySelector(".text_producto");
        elemento.innerHTML = '<i class="fas fa-info-circle text_producto">'+'Descripcion: ' +  data.nombre +' '+ data.marca.nombre +' ' +
            ' '+ '<span class="badge badge-dark">'+parseInt(data.stock)+'</span>'+'</i>'
        calcularPVP();
    });

});

//funcion para limpiar el formulario del modal
function limpiarFormModal() {
    var elementoProducto = document.querySelector("#select2-id_producto-container");
    elementoProducto.innerHTML = '<span class="select2-selection__rendered" id="select2-id_producto-container" role="textbox" aria-readonly="true" title=""><span class="select2-selection__placeholder">Buscar producto</span></span>'
}

//funcion para calcular el pvp del precio ingresado por teclado
function calcularPVP() {
    var pvp = parseFloat($('input[name="pvp"]').val());
    var equivalencia = $('input[name="equivalencia"]').val();
    var t_convercion = $('select[name="tipo_conversion"]').val();
    var p_convercion = $('input[name="porcentaje_conversion"]').val();
    var pvp_medida = 0;
    var conver_stock = 0;
    if ( equivalencia === ''){
        equivalencia = 0;
        $('input[name="equivalencia"]').val(0.000)
    }
    if ( p_convercion === ''){
        p_convercion = 0;
        $('input[name="porcentaje_conversion"]').val(0.000)
    }
    if (t_convercion === 'True'){
        pvp_medida = parseFloat(pvp * equivalencia).toFixed(4);
        conver_stock = parseFloat(1 * equivalencia).toFixed(4);
        pvp_medida = parseFloat(pvp_medida-((p_convercion/100)*pvp_medida)).toFixed(4)
    } else if(t_convercion === 'False'){
        if (equivalencia > 0){
            pvp_medida = parseFloat(pvp / equivalencia).toFixed(4);
            conver_stock = parseFloat(1 / equivalencia).toFixed(4);
            pvp_medida = parseFloat(((p_convercion / 100)+1)*pvp_medida).toFixed(4);
        }else{
            pvp_medida = 0.000
            conver_stock = 0.000
        }
    }
    $('input[name="pvp_medida"]').val(pvp_medida);
    $('input[name="conversion_stock"]').val(conver_stock);
}
