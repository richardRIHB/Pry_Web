var tblProductos;
var compra_diccionario = {
    items : {
        compra: '',
        proveedor: '',
        fecha: '',
        subtotal: 0.00,
        iva_base: 0.00,
        iva: 0.00,
        total:0.00,
        productos:[]
    },
    calcular_compra: function (){
        var subtotal = 0.00;
        var iva = $('input[name="iva"]').val();
        $.each(this.items.productos, function (posicion, dictado) {
            dictado.subtotal = dictado.cantidad_inicial * parseFloat(dictado.precio_new);
            subtotal += dictado.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * iva
        this.items.total = this.items.subtotal + this.items.iva;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },

    list: function () {
        tblProductos = $('#tblProductos').DataTable({
            lengthMenu: [[5, 10, 25, 50, 100], [5, 10, 25, 50, 100]],
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            order: [],
            data: this.items.productos,
            columns: [
                {"data": "nombre"},
                {"data": "precio_new"},
                {"data": "cantidad"},
                {"data": "cantidad"},
                {"data": "subtotal"},
                {"data": "produc.cantidad_inicial"},
            ],
            columnDefs: [

                {
                    targets: [0],
                    orderable: false,
                    render: function (data, type, row) {
                        data2 = data + '-' + row.marca.nombre + '-' + row.descripcion
                        html = data2.substr(0, 40);
                        return html;
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$'+parseFloat(data).toFixed(3);
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="stock" class="form-control form-control-sm input-sm" autocomplete="off" value="' + parseInt(data) + '" hidden>' + '<span  class="badge badge-success" id="stock" >' + parseInt(data) + '</span>'
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm"  autocomplete="off" value="'+row.cantidad_inicial+'">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$'+parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                         return '<input type="checkbox" name="estado_devolucion" value="activo" class="form-control form-control-sm input-sm" >';
                    }
                }
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex){
                console.log(data.cantidad_inicial);
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min:0,
                    max: data.cantidad,
                    step: 1,
                })
            },
            initComplete: function (settings, json) {
            }
        });
    }
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
    if (repo.estado_devolucion_c === true) {
        estado_d = 'Registrada'
        html_d = '<span  class="badge badge-success" >' + estado_d + '</span>'
    }
    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.proveedor.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Factura Nº:</b> ' + repo.id + '<br>' +
        '<b>Proveedor:</b> ' + repo.proveedor.proveedor + '<br>' +
        '<b>Estado de Devolucion:</b> ' + html_d  + '<br>' +
        '<b>Estado:</b> ' + html + '<b> &nbsp;  Total:</b> <span class="badge bg-dark">' + '$' + repo.total + '</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function () {

    $('#fecha').datetimepicker({
        format: 'DD-MM-YYYY',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        maxDate: moment().format("YYYY-MM-DD")
    });

    $("input[name='iva']").TouchSpin({
        min:0,
        max: 0.15,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function () {
        $("input[name='iva']").val(compra_diccionario.items.iva_base)
        compra_diccionario.calcular_compra();
    }).val(compra_diccionario.items.iva_base);
    
    //Evento cantidad
    $('#tblProductos tbody')
        .on('change', 'input[name="cantidad"]',function () {
            var cant = parseInt($(this).val());
            var tr = tblProductos.cell($(this).closest('td, li')).index();
            var data = tblProductos.row(tr.row).node();
            if (cant){
                compra_diccionario.items.productos[tr.row].cantidad_inicial = cant;
                compra_diccionario.calcular_compra()
                $('td:eq(4)',tblProductos.row(tr.row).node()).html('$'+compra_diccionario.items.productos[tr.row].subtotal.toFixed(2));
            }else{
                $(this).val(0)
                compra_diccionario.items.productos[tr.row].cantidad_inicial = 0;
                compra_diccionario.calcular_compra()
                $('td:eq(4)',tblProductos.row(tr.row).node()).html('$'+compra_diccionario.items.productos[tr.row].subtotal.toFixed(2));
            }
        })
        .on('change', 'input[name="estado_devolucion"]',function () {
            var estado_d = $(this).val();
            var tr = tblProductos.cell($(this).closest('td, li')).index();
            var data = tblProductos.row(tr.row).node();
            if( $(this).prop('checked') ) {
                compra_diccionario.items.productos[tr.row].cantidad_inicial = compra_diccionario.items.productos[tr.row].cantidad;
                compra_diccionario.items.productos[tr.row].estado_devolucion = true;
                compra_diccionario.calcular_compra()
                $('td:eq(4)',tblProductos.row(tr.row).node()).html('$'+compra_diccionario.items.productos[tr.row].subtotal.toFixed(2));
                $('td:eq(3)',tblProductos.row(tr.row).node()).html(compra_diccionario.items.productos[tr.row].cantidad_inicial);
            }else{
                compra_diccionario.items.productos[tr.row].cantidad_inicial = 0
                compra_diccionario.items.productos[tr.row].estado_devolucion = false;
                compra_diccionario.calcular_compra()
                $('td:eq(4)',tblProductos.row(tr.row).node()).html('$'+compra_diccionario.items.productos[tr.row].subtotal.toFixed(2));
                $('td:eq(3)',tblProductos.row(tr.row).node()).html('<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="0">');
                $('input[name="cantidad"]').TouchSpin({
                    min:0,
                    max: compra_diccionario.items.productos[tr.row].cantidad,
                    step: 1,
                })
            }
        });
    
    // Evento submit
    $('form').on('submit', function (e) {
        e.preventDefault();
        if(compra_diccionario.items.productos.length === 0){
            message_error('Seleccione una Factura de Compra en su detalle de productos')
            return false;
        }
        if(compra_diccionario.items.total === 0){
            message_error('Debe al menos devolver algun producto en su detalle de productos')
            return false;
        }
        compra_diccionario.items.fecha = $('input[name="fecha"]').val();
        compra_diccionario.items.compra = $('input[name="compra"]').val();
        compra_diccionario.items.proveedor = $('input[name="proveedor_text"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('compra_diccionario', JSON.stringify(compra_diccionario.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
            alert_action('Notificacion', '¿Desea imprimir la Devolucion de Compra?', function () {
                window.open('/App_Facturacion/devolucion/compra/pdf/'+ response.id +'/', '_blank');
                location.href = '/App_Facturacion/devolucion/compra/list/';
            }, function () {
                location.href = '/App_Facturacion/devolucion/compra/list/';
            });
        });
    });

    // Busqueda de compras con select2
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear:true,
        ajax:{
            delay: 250,
            type:'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_compra'
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
            if (data.estado_devolucion_c === false){
                $('input[name="proveedor_text"]').val(data.proveedor.proveedor);
                $('input[name="compra"]').val(data.id);
                $('input[name="iva"]').val(data.iva_base);
                compra_diccionario.items.productos = data.produc;
                compra_diccionario.items.iva_base = data.iva_base;
                compra_diccionario.list()
                compra_diccionario.calcular_compra();
                $(this).val('').trigger('change.select2');
            } else {
                message_error('Esta Factura de Compra ya esta registrada en Devoluciones')
            }
        } else {
            message_error('Esta Factura de Compra esta anulada')
        }
    });

    compra_diccionario.list();
});
