var tblCompra;

function get_data() {
    tblCompra = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        order: [],
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
            {"data": "proveedor.proveedor"},
            {"data": "fecha"},
            {"data": "total"},
            {"data": "estado"},
            {"data": "tipo_documento"},
            {"data": "total"},
        ],
        columnDefs: [
            {
                targets: [1],
                render: function (data, type, row) {
                    return '<a>' + row.proveedor.proveedor + '</a>';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="detalle" class="bg-success btn-xs"><i class="fas fa-search"></i>Items</a> ';
                    if (row.estado === true){
                        if (row.tipo_documento === true) {
                                buttons += '<a href="/App_Facturacion/compra/update/' + row.id + '/" class="bg-info btn-xs " ><i class="fas fa-edit"></i> Facturar</a> ';
                        } else {
                                buttons += '<a href="/App_Facturacion/compra/pdf/' + row.id + '/" class="bg-dark btn-xs" target="_blank"><i class="fas fa-print"></i> Imprimir</a> ';
                                buttons += '<a rel="delete"  class="bg-danger btn-xs"><i class="fas fa-trash-alt"></i> Anular</a> '
                        }
                    }
                    return buttons;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var tipo_documen = 'Factura'
                    var html = '<span  class="badge badge-info" >' + tipo_documen + '</span>'
                    if (row.tipo_documento === true) {
                        tipo_documen = 'Proforma'
                        html = '<span  class="badge badge-primary" >' + tipo_documen + '</span>'
                    }
                    return html
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var estado = 'Anulado'
                    var html = '<span  class="badge badge-danger" >' + estado + '</span>'
                    if (row.estado === true) {
                        estado = 'Activo'
                        html = '<span  class="badge badge-success" >' + estado + '</span>'
                    }
                    return html
                }
            },
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-5],
                class: 'text-center',
                render: function (data, type, row) {
                    return data;
                }
            },
        ],
        initComplete: function (settings, json) {

        }

    });
};

$(function () {
    get_data();
    //Limpiar el modal al dar click en cerrar
    $('.cerrarModal').on('click', function () {
        limpiarFormModal();
    });

    $('#data tbody')
        .on('click', 'a[rel="detalle"]', function () {
            var tr = tblCompra.cell($(this).closest('td, li')).index();
            var data = tblCompra.row(tr.row).data();

            $('#tbldetalle').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_detalle_producto',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "producto.nombre"},
                    {"data": "precio"},
                    {"data": "cantidad"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [0],
                        render: function (data, type, row) {
                             html = data+' '+row.producto.marca.nombre+' '+row.producto.descripcion;
                             html = html.substr(0, 85);
                            return html;
                        }
                    },
                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [-3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + data;
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '<span  class="badge badge-success" >' + parseFloat(data).toFixed(0) + '</span>';
                        }
                    },
                ],
                initComplete: function (settings, json) {
                }
            });

            $('#myModalDetalle').modal('show');
        })
        .on('click', 'a[rel="delete"]', function () {
            // e.preventDefault();
            var tr = tblCompra.cell($(this).closest('td, li')).index();
            var data = tblCompra.row(tr.row).data();
            var parameters = new FormData();
            if(data.estado_devolucion_c === true){
                message_error('No se puede anular la Factura de Compra  Nº '+' <span  class="badge badge-success" > '+ data.id + '</span>'+' debido a que se encuentra registrado en el Modulo Devoluciones')
                return false;
            }
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de anular la Fatura de Compra Nº'+' <span  class="badge badge-success" > '+ data.id + '</span>' +'?', parameters, function () {
                tblCompra.ajax.reload();
            });
        });
});

//funcion para limpiar el formulario del modal
function limpiarFormModal() {
    $('form')[0].reset();
    $('#myModalDetalle').modal('hide');
}
