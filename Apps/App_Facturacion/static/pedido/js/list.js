$(function () {
    tblPedido = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        order: [[0, "desc"]],
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "venta.id"},
            {"data": "venta.cliente.cliente"},
            {"data": "fecha"},
            {"data": "fecha_entrega"},
            {"data": "estado"},
            {"data": "estado_entrega"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                render: function (data, type, row) {
                    var estado = 'Anulado'
                    var html = '<span  class="badge badge-danger sorting" >' + estado + ' </span>'
                    if (row.estado === true) {
                        estado = 'Activo'
                        html = '<span  class="badge badge-success sorting" >' + estado + ' </span>'
                    }
                    return html
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    var estado_entrega = 'Pendiente'
                    var html = '<span  class="badge badge-warning sorting" >' + estado_entrega + ' </span>'
                    if (row.estado_entrega === true) {
                        estado_entrega = 'Entregado'
                        html = '<span  class="badge badge-success sorting" >' + estado_entrega + ' </span>'
                    }
                    return html
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/App_Facturacion/pedido/recibo/' + row.id + '" class="bg-dark btn-xs" target="_blank"><i class="fas fa-print"></i> Imprimir</a> ';
                    if (row.estado === true) {
                        if (row.estado_entrega === false){
                            buttons += '<a rel="confirmar" class="bg-success btn-xs"><i class="fas fa-check"></i> Confirmar</a> ';
                            buttons += '<a rel="anular"  class="bg-danger btn-xs"><i class="fas fa-trash-alt"></i> Anular</a> ';
                        }

                    }
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('#data tbody')
        .on('click', 'a[rel="anular"]', function () {

            var tr = tblPedido.cell($(this).closest('td, li')).index();
            var data = tblPedido.row(tr.row).data();
            console.log(data);
            var parameters = new FormData();
            parameters.append('action', 'anular');
            parameters.append('id', data.id);

            submit_with_ajax(window.location.pathname, 'Notificación', '¿Desea anular el Pedido N° <span  class="badge badge-success sorting">' + data.venta.id + '</span> ?', parameters, function (response) {
                location.href = '/App_Facturacion/pedido/list/';
            });
        })
        .on('click', 'a[rel="confirmar"]', function () {

            var tr = tblPedido.cell($(this).closest('td, li')).index();
            var data = tblPedido.row(tr.row).data();
            console.log(data);
            var parameters = new FormData();
            parameters.append('action', 'confirmar');
            parameters.append('id', data.id);

            submit_with_ajax(window.location.pathname, 'Notificación', '¿Confirman entrega del Pedido N° <span  class="badge badge-success sorting">' + data.venta.id + '</span> ?', parameters, function (response) {
                location.href = '/App_Facturacion/pedido/list/';
            });
        })
});