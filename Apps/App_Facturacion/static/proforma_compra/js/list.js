var tblCompra;

function get_data() {
    tblCompra = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        order: [[ 0, "desc" ]],
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
            {"data": "subtotal"},
            {"data": "iva"},
            {"data": "total"},
            {"data": "total"},
        ],
        columnDefs: [
            {
                targets: [1],
                orderable: false,
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
                    buttons += '<a href="/App_Facturacion/proforma/compra/update/' + row.id + '/" class="bg-warning btn-xs " ><i class="fas fa-edit"></i> Editar</a> ';
                    buttons += '<a href="/App_Facturacion/proforma/compra/pdf/' + row.id + '/" class="bg-dark btn-xs" target="_blank"><i class="fas fa-print"></i> Imprimir</a> ';
                    return buttons;
                }
            },
            {
                targets: [-2, -3, -4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-5],
                class: 'text-center',
                orderable: false,
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
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '<span  class="badge badge-success" >' + parseFloat(data).toFixed(0) + '</span>';
                        }
                    },
                    {
                        targets: [-3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(3);
                        }
                    },
                ],
                initComplete: function (settings, json) {
                }
            });

            $('#myModalDetalle').modal('show');
        })
});

//funcion para limpiar el formulario del modal
function limpiarFormModal() {
    $('form')[0].reset();
    $('#myModalDetalle').modal('hide');
}
