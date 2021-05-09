function format(d) {
    var html = '<table class="table">';
    html += '<thead class="thead-dark">';
    html += '<tr><th scope="col">Producto</th>';
    html += '<th scope="col">Descripcion</th>';
    html += '<th scope="col">PVP</th>';
    html += '<th scope="col">Cantidad</th>';
    html += '<th scope="col">Subtotal</th></tr>';
    html += '</thead>';
    html += '<tbody>';
    $.each(d.det, function (key, value) {
        html += '<tr>'
        html += '<td>' + value.producto.nombre + '</td>'
        html += '<td>' + value.producto.descripcion + '</td>'
        html += '<td>' + value.precio + '</td>'
        html += '<td>' + value.cantidad + '</td>'
        html += '<td>' + value.subtotal + '</td>'
        html += '</tr>';
    });
    html += '</tbody>';
    return html;
}

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
            {"data": "id"},
            {"data": "cliente.cliente"},
            {"data": "fecha"},
            {"data": "total"},
            {"data": "estado"},
            {"data": "tipo_documento"},
            {"data": "id"},

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
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var estado = 'Anulada'
                    var html = '<span  class="badge badge-danger" >' + estado + '</span>'
                    if (row.estado === true) {
                        estado = 'Activa'
                        html = '<span  class="badge badge-success" >' + estado + '</span>'
                    }
                    return html
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var tipo_documento = 'Factura'
                    var html = '<span  class="badge badge-info" >' + tipo_documento + '</span>'
                    if (row.tipo_documento === true) {
                        tipo_documento = 'Proforma'
                        html = '<span  class="badge badge-primary" >' + tipo_documento + '</span>'
                    }
                    return html
                }
            },
            {
                targets: [-1],
                class: 'text-left',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="details" class="bg-success btn-xs"><i class="fas fa-search"></i> Items</a> ';
                    if (row.estado === true) {
                        if (row.tipo_documento === true) {
                            buttons += '<a href="/App_Facturacion/venta/update/' + row.id + '/" class="bg-info btn-xs " ><i class="fas fa-edit"></i> Facturar</a> ';
                        } else {
                            if (row.estado_pedido ===false){
                                buttons += '<a rel="pedido" class="bg-warning btn-xs"  ><i class="fas fa-truck"></i> Pedido</a> ';
                            }
                            buttons += '<a href="/App_Facturacion/venta/factura/pdf/' + row.id + '/" class="bg-dark btn-xs " target="_blank"><i class="fas fa-print"></i> Imprimir</a> ';
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

            var tr = tblSale.cell($(this).closest('td, li')).index();
            var data = tblSale.row(tr.row).data();
            var parameters = new FormData();
            if(data.estado_devolucion === true){
                message_error('No se puede anular la Factura Nº '+' <span  class="badge badge-success" > '+ data.id + '</span>'+' debido a que se encuentra registrado en el Modulo Devoluciones')
                return false;
            }
            parameters.append('action', 'anular');
            parameters.append('id', data.id);

            submit_with_ajax(window.location.pathname, 'Notificación', '¿Desea anular la Factura N° ' + data.id + '?', parameters, function (response) {
                location.href = '/App_Facturacion/venta/list/';
            });
        })

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
                        targets: [1],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return data;
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
                ],
                initComplete: function (settings, json) {
                }
            });

            $('#myModelDet').modal('show');
        })
        .on('click', 'td.details-control', function () {
            var tr = $(this).closest('tr');
            var row = tblSale.row(tr);
            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            } else {
                row.child(format(row.data())).show();
                tr.addClass('shown');
            }
        })

        .on('click', 'a[rel="pedido"]', function () {
            $('input[name="action"]').val('add');
            $('form')[0].reset();
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var data = tblSale.row(tr.row).data();
            modal_title.find('span').html('Creación de un Pedido');
            modal_title.find('i').removeClass().addClass('fas fa-plus');
            $('input[name="fecha_entrega"]').val(moment().format("DD-MM-YYYY HH:mm A"));
            $('#id_fecha_entrega').datetimepicker({
                format: 'DD-MM-YYYY HH:mm A',
                date: moment().format("YYYY-MM-DD HH:mm "),
                locale: 'es',
                minDate: moment().format("YYYY-MM-DD HH:mm ")
            });
            $("input[name='total']").TouchSpin({
                min: 0,
                max: 100,
                step: 0.01,
                decimals: 2,
                boostat: 5,
                maxboostedstep: 10,
                prefix: 'USD $'
            }).on('change', function () {
                if (isNaN(parseFloat($(this).val()))) {
                    $(this).val(0.00);
                }
            }).val();

            $('#span_venta').html(data.id);
            $('#id_direccion').val(data.cliente.direccion);
            $('#id_ubicacion_link').val(data.cliente.ubicacion_link);
            $("input[name='ubicacion']").val(data.cliente.ubicacion);
            $('#myModalPedido').modal('show');
            $("input[name='venta']").val(data.id);

        });

    //Modal de Pedido
    modal_title = $('.modal-title');
    $('#myModalPedido').on('shown.bs.modal', function () {
         // $('form')[0].reset();
    });

    $('form').on('submit', function (e) {
        e.preventDefault();
        filtrar_ubicacion_iframe()
        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#myModalPedido').modal('hide');
            tblSale.ajax.reload();
        });
    });
});

function filtrar_ubicacion_iframe() {
    var ubicacion = $('input[name="ubicacion"]').val();
    if (ubicacion.length !== 0){
        ubicacion=ubicacion.replace('<iframe src="','');
        ubicacion=ubicacion.replace('" width="600" height="450" frameborder="0" style="border:0;" allowfullscreen="" aria-hidden="false" tabindex="0"><','');
        ubicacion=ubicacion.replace('/iframe>','');
        $('input[name="ubicacion"]').val(ubicacion);
    }
}