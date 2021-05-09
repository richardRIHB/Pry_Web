var tblProducts;
var vents = {
    items: {
        cliente: '',
        fecha: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: [],
        metodo_pago: true,
        tipo_documento: false,
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        var iva = $('input[name="iva"]').val();
        var cambio = 0.00;
        $.each(this.items.products, function (pos, dict) {
            dict.pos = pos;
            pvp_item = parseFloat(dict.pvp_medida).toFixed(2) - parseFloat(dict.descuento);
            dict.subtotal = parseFloat(pvp_item).toFixed(2) * dict.cantidad;
            subtotal += dict.subtotal;
        });

        this.items.subtotal = parseFloat(subtotal) / (parseFloat(iva) + 1);
        this.items.iva = this.items.subtotal * iva;
        this.items.total = subtotal;
        cambio = ($('input[name="valor_recibido"]').val()) - subtotal;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
        $('input[name="valor_cambio"]').val(cambio.toFixed(2));
    },
    add: function (item) {
        var aux = false;
        $.each(this.items.products, function (pos, dict) {
            dict.pos = pos;
            if (dict.id === item.id) {
                Swal.fire('Notificación', '<strong>ITEM YA AGREGADO:  </strong> Verificar lista de ITEMS');
                aux = true;
            }
        });
        stock_r = parseInt(item.producto.stock)
        cant_real = stock_r / item.conversion_stock
        if (parseInt(cant_real)>=1 && aux === false){
            this.items.products.push(item);
            this.list();
        } else if(parseInt(cant_real)<1) {
            Swal.fire('Notificación', '<strong>STOCK INSUFICIENTE:  </strong> Verificar el STOCK');
        }
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
                {"data": "cantidad"},
                {"data": "producto.nombre"},
                {"data": "pvp_medida"},
                {"data": "producto.stock"},
                {"data": "descuento"},
                {"data": "subtotal"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
                    }
                },
                {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        html = row.producto.nombre + ' - ' + row.producto.marca.nombre + ' - ' + row.medida
                        return html;
                    }
                },
                {
                    targets: [2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        pvp_item = parseFloat(data).toFixed(2) - parseFloat(row.descuento);
                        return '$' + parseFloat(pvp_item).toFixed(2);
                    }
                },
                {
                    targets: [3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        stock_r = parseInt(data)
                        cant_real = stock_r / row.conversion_stock
                        return '<input type="text" name="stock" class="form-control form-control-sm input-sm" autocomplete="off" value="' + parseFloat(data).toFixed(2) + '" hidden>' + '<span  class="badge badge-success" id="stock" >' + parseInt(cant_real) + '</span>'
                    }
                },
                {
                    targets: [4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="desc" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.descuento + '">';
                    }
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
                        return '<a rel="remove" class="btn btn-danger btn-xs " style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },

            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                stock_r = parseInt(data.producto.stock)
                cant_real = stock_r / data.conversion_stock
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: parseInt(cant_real),
                    step: 1
                });
                $(row).find('input[name="desc"]').TouchSpin({
                    min: 0.00,
                    decimals: 2,
                    max: 1000,
                    step: 0.01
                });
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
    stock_r = parseInt(repo.producto.stock)
    cant_real = stock_r / repo.conversion_stock
    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.producto.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        repo.producto.nombre + ' ' + repo.producto.marca.nombre + ' ' + repo.producto.descripcion.substr(0, 70) + '<br>' +
        '<b>PVP:</b> <span class="badge badge-warning">$' + parseFloat(repo.pvp_medida).toFixed(2) + '</span>' +
        '<b>    STOCK:</b> <span class="badge badge-success">' + parseInt(cant_real) + '</span>' +
        '<b>    MEDIDA:</b> <span class="badge badge-dark">' + repo.medida + '</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

function formatRepo_cliente(repo) {
    if (repo.loading) {
        return repo.text;
    }
    var estado = 'Bloqueado'
    var html = '&nbsp<span  class="badge badge-warning" >' + estado + '</span>'
    if (repo.estado === true) {
        estado = 'Activo'
        html = '&nbsp<span  class="badge badge-success" >' + estado + '</span>'
    }

    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<i class="fas fa-user-tag "></i>' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>&nbsp' + repo.cliente + '</b><br>' +
        '<b>C.I:</b> ' + repo.c_i + html +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function () {
    modal_title = $('.modal-title');

    $('#id_descripcion_credito').hide();
    $('#id_lbl_descripcion').hide();

    $('select[name="cliente"]').select2({
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
                    action: 'search_clientes'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Buscar Cliente',
        minimumInputLength: 1,
        templateResult: formatRepo_cliente,
    });

    $('#fecha').datetimepicker({
        format: 'YYYY-MM-DD HH:mm',
        date: moment().format("YYYY-MM-DD HH:mm"),
        locale: 'es',
        minDate: moment().format("YYYY-MM-DD HH:mm")
    });

    $('#id_metodo_pago').on('change', function () {
        if ($(this).prop("checked")) {
            $('#id_lbl_descripcion').show();
            $('#id_descripcion_credito').show();
        } else {
            $('#id_descripcion_credito').hide();
            $('#id_lbl_descripcion').hide();
        }
    });


    $("input[name='valor_recibido']").TouchSpin({
        min: 0.00,
        max: 10000,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '$USD'
    }).on('change', function () {
        if (isNaN(parseFloat($(this).val()))) {
            $(this).val(0.00);
        }
        vents.calculate_invoice();
    }).val(0.00);
    $('.btnAddClient').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de un cliente');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('#myModalClient').modal('show');
    });

    $('#myModalClient').on('hidden.bs.modal', function () {
        $('#frm_cliente').trigger('reset');
    });

    $('#frm_cliente').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'add_cliente');
        parameters.append('ruc', '');
        parameters.append('celular', '');
        parameters.append('estado', 'True');
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de crear al siguiente cliente?', parameters, function (response) {
                console.log(response)
                var newOption = new Option(response.cliente, response.id, false, true);
                $('select[name="cliente"]').append(newOption).trigger('change');
                $('#myModalClient').modal('hide');
            });
    });


    $('.btnRemoveAll').on('click', function () {
        if (vents.items.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle de productos?', function () {
            vents.items.products = [];
            vents.list();
        }, function () {

        });
    });

    // event cant
    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            var data = vents.items.products[tr.row];
            alert_action('Notificación', '¿Estas seguro de eliminar el producto: ' + '<strong>' + data.producto.nombre + ' ' + data.producto.marca.nombre + '</strong>' + ' ' + ' <span  class="badge badge-success" > ' + data.medida + '</span>' + ' de tu detalle de productos?', function () {
                vents.items.products.splice(tr.row, 1);
                vents.list();
            }, function () {

            });
        })
        .on('change', 'input[name="cant"]', function () {
            if (isNaN(parseFloat($(this).val()))) {
                $(this).val(1);
            }
            var cantidad = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            var data = vents.items.products[tr.row];
            var stock_r = parseInt(data.producto.stock)
            var stock_real = parseInt(stock_r / data.conversion_stock)

            if (cantidad > stock_real) {
                vents.items.products[tr.row].cantidad = stock_real;
                Swal.fire('Notificación', '<strong>Stock insuficiente:  </strong> Verificar cantidad a vender');
                $(this).val(stock_real);
            } else {
                vents.items.products[tr.row].cantidad = cantidad;
            }
            vents.calculate_invoice();
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));
        })
        .on('change', 'input[name="desc"]', function () {
            if (isNaN(parseFloat($(this).val()))) {
                $(this).val(0.00);
            }
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            var data = vents.items.products[tr.row];

            pvp_item = parseFloat(data.pvp_medida) - parseFloat($(this).val());

            pvp_bruto_iva = parseFloat(data.producto.precio_bruto) * (parseFloat(data.producto.iva) + 1);
            if (data.tipo_conversion) {
                pvp_bruto_iva = parseFloat(pvp_bruto_iva) * parseFloat(data.equivalencia);
            } else {
                pvp_bruto_iva = parseFloat(pvp_bruto_iva) / parseFloat(data.equivalencia);
            }
            if (pvp_item < pvp_bruto_iva) {
                Swal.fire('Notificación', '<strong>VERIFICAR DESCUENTO:  </strong> Descuento supera el limite maximo permitido');
                desc_max = parseFloat(data.pvp_medida) - parseFloat(pvp_bruto_iva);
                vents.items.products[tr.row].descuento = parseFloat(desc_max).toFixed(2);
                $(this).val(desc_max.toFixed(2))
            } else {
                vents.items.products[tr.row].descuento = parseFloat($(this).val());
            }

            vents.calculate_invoice();
            pvp_item=parseFloat(data.pvp_medida) - parseFloat($(this).val());
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));
            $('td:eq(2)', tblProducts.row(tr.row).node()).html('$' + pvp_item.toFixed(2));

        });

    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    // event submit
    $('#frm_venta').on('submit', function (e) {
        e.preventDefault();

        if (vents.items.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }

        vents.items.fecha = $('input[name="fecha"]').val();
        vents.items.cliente = $('select[name="cliente"]').val();
        vents.items.metodo_pago = document.getElementById('id_metodo_pago').checked;
        vents.items.descripcion = $('#id_descripcion_credito').val();

        if (vents.items.cliente.length === 0) {
            message_error('Seleccione un Cliente');
            return false;
        }

        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('iva_base', $('input[name="iva"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
            alert_action('Notificación', '¿Desea imprimir la boleta de venta?', function () {
                window.open('/App_Facturacion/venta/factura/pdf/' + response.id + '/', '_blank');
                location.href = '/App_Facturacion/venta/list/';
            }, function () {
                location.href = '/App_Facturacion/venta/list/';
            });
        });
    });

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
                    action: 'search_products'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        data.cantidad = 1;
        data.subtotal = 0.00;
        data.descuento = 0.00;
        vents.add(data);
        $(this).val('').trigger('change.select2');
    });
})
;