var tblProducts;
var vents = {
    items: {
        venta: '',
        cliente: '',
        fecha: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: [],
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        var iva = $('input[name="iva"]').val();
        $.each(this.items.products, function (pos, dict) {
            dict.pos = pos;
            dict.subtotal = parseFloat(dict.precio).toFixed(2) * dict.cantidad_inicial;
            subtotal += dict.subtotal;
        });

        this.items.subtotal = parseFloat(subtotal) / (parseFloat(iva) + 1);
        this.items.iva = this.items.subtotal * iva;
        this.items.total = subtotal;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },

    list: function () {
        this.calculate_invoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            order: [],
            data: this.items.products,
            columns: [
                {"data": "producto.nombre"},
                {"data": "precio"},
                {"data": "descuento"},
                {"data": "cantidad"},
                {"data": "cantidad"},
                {"data": "subtotal"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    orderable: false,
                    render: function (data, type, row) {
                        html = data + ' - ' + row.producto.marca.nombre + ' - ' + row.medida
                        return html;
                    }
                },
                {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + data;
                    }
                },
                {
                    targets: [2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' +data;
                    }
                },
                {
                    targets: [3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span  class="badge badge-success" id="stock" >' + data + '</span>';
                    }
                },
                {
                    targets: [4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm"  autocomplete="off" value="'+row.cantidad_inicial+'">';                    }
                },
                {
                    targets: [5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [6],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="checkbox" name="estado_devolucion" value="activo" class="form-control form-control-sm input-sm" >';
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min:0,
                    max: data.cantidad,
                    step: 1,
                })
            },
            initComplete: function (settings, json) {

            }
        });
    },
};

function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var estado = 'Anulada'
    var html = '<span  class="badge badge-danger" >' + estado + '</span>'
    if (repo.estado === true) {
        estado = 'Activa'
        html = '<span  class="badge badge-success" >' + estado + '</span>'
    }
    var estado_d = 'No Registrada'
    var html_d = '<span  class="badge badge-warning" >' + estado_d + '</span>'
    if (repo.estado_devolucion === true) {
        estado_d = 'Registrada'
        html_d = '<span  class="badge badge-success" >' + estado_d + '</span>'
    }
    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<i class="fas fa-print fa-3x"></i>' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b>Factura Nº:</b> ' + repo.id + '<br>' +
        '<b>Cliente:</b> ' + repo.cliente.cliente + '<br>' +
        '<b>Estado de Devolucion:</b> ' + html_d  + '<br>' +
        '<b>Estado:</b> ' + html + '<b> &nbsp;  Total:</b> <span class="badge bg-dark">' + '$' + repo.total + '</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}


$(function () {

    $('input[name="fecha"]').val( moment().format("DD-MM-YYYY HH:mm A"));


    // event cant
    $('#tblProducts tbody')
        .on('change', 'input[name="cantidad"]', function () {
            if (isNaN(parseFloat($(this).val()))) {
                $(this).val(0);
            }
            var cantidad = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.items.products[tr.row].cantidad_inicial = cantidad;
            vents.calculate_invoice();
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));
        })
        .on('change', 'input[name="estado_devolucion"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();

            if ($(this).prop('checked')){
                vents.items.products[tr.row].cantidad_inicial = vents.items.products[tr.row].cantidad;
                vents.items.products[tr.row].estado_devolucion = true;
                vents.calculate_invoice()
                $('td:eq(5)',tblProducts.row(tr.row).node()).html('$'+vents.items.products[tr.row].subtotal.toFixed(2));
                $('td:eq(4)',tblProducts.row(tr.row).node()).html(vents.items.products[tr.row].cantidad_inicial);
            }else{
                vents.items.products[tr.row].cantidad_inicial = 0
                vents.items.products[tr.row].estado_devolucion = false;
                vents.calculate_invoice()
                $('td:eq(5)',tblProducts.row(tr.row).node()).html('$'+vents.items.products[tr.row].subtotal.toFixed(2));
                $('td:eq(4)',tblProducts.row(tr.row).node()).html('<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="0">');
                $('input[name="cantidad"]').TouchSpin({
                    min:0,
                    max: vents.items.products[tr.row].cantidad,
                    step: 1,
                })
            }
        });

    // event submit
    $('form').on('submit', function (e) {
        e.preventDefault();
        if(vents.items.products.length === 0){
            message_error('Seleccione una Factura de Compra en su detalle de productos')
            return false;
        }
        if(vents.items.total === 0){
            message_error('Debe al menos devolver algun producto en su detalle de productos')
            return false;
        }

        vents.items.fecha = $('input[name="fecha"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('iva_base', $('input[name="iva"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
            alert_action('Notificación', '¿Desea imprimir la boleta de Devolucion?', function () {
                window.open('/App_Facturacion/devolucion/factura/pdf/' + response.id + '/', '_blank');
                location.href = '/App_Facturacion/devolucion/list/';
            }, function () {
                location.href = '/App_Facturacion/devolucion/list/';
            });
        });
    });

    // Buscar factura;
    $('select[name="search"]').select2({
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
                    action: 'search_venta'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese un Nº de Factura',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        if (data.estado === true){
            if (data.estado_devolucion === false){
                console.log(data)
                $('input[name="cliente_text"]').val(data.cliente.cliente);
                $('input[name="venta"]').val(data.id);
                $('input[name="iva"]').val(data.iva_base);
                vents.items.products = data.produc;
                vents.items.venta = data.id;
                vents.list()
                vents.calculate_invoice();
                $(this).val('').trigger('change.select2');
            } else {
                message_error('Esta Factura ya esta registrada en Devoluciones')
            }
        } else {
            message_error('Esta Factura esta anulada')
        }
    });
});