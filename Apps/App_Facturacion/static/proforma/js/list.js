
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

            {"data": "id",},
            {"data": "cliente.cliente"},
            {"data": "fecha"},
            {"data": "total"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-2],
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
                    var buttons = '<a rel="details" class="bg-success btn-xs"><i class="fas fa-search"></i> Items</a> ';
                        buttons += '<a href="/App_Facturacion/proforma/update/' + row.id + '/" class="bg-warning btn-xs"  ><i class="fas fa-edit"></i> Editar</a> ';
                        buttons += '<a href="/App_Facturacion/proforma/factura/pdf/' + row.id + '/" class="bg-dark btn-xs " target="_blank"><i class="fas fa-print"></i> Imprimir</a> ';
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

});