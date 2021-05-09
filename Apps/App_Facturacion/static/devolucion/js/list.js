
$(function () {
    tblSale = $('#data').DataTable({
        responsive: true,
        scrollX: true,
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

            {"data": "venta.id",},
            {"data": "venta.cliente.cliente"},
            {"data": "fecha"},
            {"data": "iva"},
            {"data": "subtotal"},
            {"data": "total"},
            {"data": "estado"},
            {"data": "total"},
        ],
        columnDefs: [
            {
                targets: [1],
                orderable: false,
                render: function (data, type, row) {
                    return data;
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
                targets: [-3,-4,-5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-2],
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
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="details" class="bg-success btn-xs"><i class="fas fa-search"></i> Items</a> ';
                    if (row.estado === true){
                        buttons += '<a href="/App_Facturacion/devolucion/factura/pdf/' + row.id + '/" class="bg-dark btn-xs " target="_blank"><i class="fas fa-print"></i> Imprimir</a> ';
                        buttons += '<a rel="delete"  class="bg-danger btn-xs"><i class="fas fa-trash-alt"></i> Anular</a> '
                    }
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('#data tbody')
        .on('click', 'a[rel="details"]', function () {

            var tr = tblSale.cell($(this).closest('td, li')).index();
            var data = tblSale.row(tr.row).data();

            $('#tblDet').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                order: [],
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_details_prod',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "inventario.producto.nombre"},
                    {"data": "inventario.medida"},
                    {"data": "precio"},
                    {"data": "descuento"},
                    {"data": "cantidad"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [0],
                        orderable: false,
                        render: function (data, type, row) {
                            html=data+' '+row.inventario.producto.marca.nombre+' '+row.inventario.producto.descripcion;
                            html = html.substr(0, 66);
                            return html;
                        }
                    },
                    {
                        targets: [-1,-3,-4],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '<span  class="badge badge-success" >' + data + '</span>';
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
            $('#myModelDet').modal('show');
        })
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var data = tblSale.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de anular la Devolucion de Venta Nº'+' <span  class="badge badge-success" > '+ data.venta.id + '</span>' +'?', parameters, function () {
                tblSale.ajax.reload();
            });
        });
});