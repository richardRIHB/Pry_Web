var tblProductos;
var compra_diccionario = {
    items : {
        proveedor: '',
        fecha: '',
        subtotal: 0.00,
        iva: 0.00,
        iva_base: 0.00,
        total: 0.00,
        productos:[]
    },
    ids_productos: function(){
        var ids = [];
        $.each(this.items.productos, function (key, value) {
            ids.push(value.id)
        });
        return ids
    },
    calcular_compra: function (){
        var subtotal = 0.00;
        $.each(this.items.productos, function (posicion, dictado) {
            dictado.subtotal = dictado.cantidad * parseFloat(dictado.precio_new);
            subtotal += dictado.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * this.items.iva_base
        this.items.total = this.items.subtotal + this.items.iva;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function (item){
        this.items.productos.push(item);
        this.list();
    },
    list: function () {
        this.calcular_compra();
        tblProductos = $('#tblProductos').DataTable({
            lengthMenu: [[5, 10, 25, 50, 100], [5, 10, 25, 50, 100]],
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            order: [],
            data: this.items.productos,
            columns: [
                {"data": "descripcion"},
                {"data": "nombre"},
                {"data": "precio_bruto"},
                {"data": "precio_new"},
                {"data": "stock"},
                {"data": "cantidad"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remover" class="btn btn-danger btn-xs btnDelete"><i class="fas fa-trash-alt"></i></a> ';
                    }
                },
                {
                    targets: [1],
                    orderable: false,
                    render: function (data, type, row) {
                        data2 = data + '-' + row.marca.nombre + '-' + row.descripcion
                        html = data2.substr(0, 30);
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
                        return '<input type="text" name="precio_new" class="form-control form-control-sm input-sm" autocomplete="off" value="'+row.precio_new+'">';

                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        resul = parseFloat(data).toFixed();
                        return '<input type="text" name="stock" class="form-control form-control-sm input-sm" autocomplete="off" value="' + parseInt(resul) + '" hidden>' + '<span  class="badge badge-success" id="stock" >' + parseInt(resul) + '</span>'
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="'+row.cantidad+'">';

                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$'+parseFloat(data).toFixed(2);

                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex){
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min:1,
                    max: 5000,
                    step: 1,
                })
                $(row).find('input[name="precio_new"]').TouchSpin({
                    min:0,
                    max: 500,
                    step: 0.001,
                    decimals: 3
                });
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
        '<p style="margin-bottom: 0;">' +
        repo.nombre + ' ' + repo.descripcion.substr(0, 70) + '<br>' +
        '<b>Marca:</b> <span class="badge bg-dark">' + repo.marca.nombre + '</span>' + ' ' +
        '<b>Estado:</b> ' + html +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

function formatRepo_proveedor(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var estado = 'Bloqueado'
    var html1 = '&nbsp<span  class="badge badge-warning" >' + estado + '</span>'
    if (repo.estado === true) {
        estado = 'Activo'
        html1 = '&nbsp<span  class="badge badge-success" >' + estado + '</span>'
    }

    var html = '<span  class="badge badge-dark" >' + repo.empresa + '</span>'

    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-2">' +
        '<img src="' + repo.imagen + '" class="img-fluid d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-10 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.proveedor + '<br>' +
        '<b>C.I:</b> ' + repo.c_i + '<br>' +
        '<b>Empresa:</b> ' + html +' '+ html1 +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function () {
    $('#id_descripcion_credito').hide();
    $('#id_lbl_descripcion').hide();

    $('select[name="proveedor"]').select2({
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
                    action: 'search_proveedor'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Buscar proveedor',
        minimumInputLength: 1,
        templateResult: formatRepo_proveedor,
    });

    $('#fecha').datetimepicker({
        format: 'DD-MM-YYYY',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        maxDate: moment().format("YYYY-MM-DD")
    })
    $('input[name="fecha"]').on('change', function () {
        if (isNaN(parseFloat($(this).val()))) {
            $(this).val(moment().format("DD-MM-YYYY"));
        }
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

    $('.btnRemoverTodo').on('click', function (){
        if (compra_diccionario.items.productos.length === 0) return false;
        alert_action('Notificación','¿Estas seguro de eliminar todos los items de tu detalle de productos?', function () {
            compra_diccionario.items.productos = [];
            compra_diccionario.list();
        }, function () {
            
        });
    });
    
    //Evento cantidad
    $('#tblProductos tbody')
        .on('click', 'a[rel="remover"]', function () {
            var tr = tblProductos.cell($(this).closest('td, li')).index();
            var data = tblProductos.row(tr.row).data();
            alert_action('Notificación','¿Estas seguro de eliminar el producto '+' <span  class="badge badge-success" > '+ data.nombre + '</span>'+' de tu detalle de productos?', function () {
                compra_diccionario.items.productos.splice(tr.row, 1);
                compra_diccionario.list();
            }, function () {
                
            });
        })
        .on('change', 'input[name="cantidad"]',function () {
            var cant = parseInt($(this).val());
            var tr = tblProductos.cell($(this).closest('td, li')).index();
            var data = tblProductos.row(tr.row).node();
            if (cant){
                compra_diccionario.items.productos[tr.row].cantidad = cant;
                compra_diccionario.calcular_compra()
                $('td:eq(6)',tblProductos.row(tr.row).node()).html('$'+compra_diccionario.items.productos[tr.row].subtotal.toFixed(2));
            }else{
                $(this).val(1)
                compra_diccionario.items.productos[tr.row].cantidad = 1;
                compra_diccionario.calcular_compra()
                $('td:eq(6)',tblProductos.row(tr.row).node()).html('$'+compra_diccionario.items.productos[tr.row].subtotal.toFixed(2));
            }
            })
        .on('change', 'input[name="precio_new"]',function () {
            var precio_n = parseFloat($(this).val());
            var tr = tblProductos.cell($(this).closest('td, li')).index();
            var data = tblProductos.row(tr.row).node();
            if(precio_n){
                compra_diccionario.items.productos[tr.row].precio_new = precio_n;
                compra_diccionario.calcular_compra()
                $('td:eq(6)',tblProductos.row(tr.row).node()).html('$'+compra_diccionario.items.productos[tr.row].subtotal.toFixed(2));
            }else{
                $(this).val('0.00')
                compra_diccionario.items.productos[tr.row].precio_new = 0.00;
                compra_diccionario.calcular_compra()
                $('td:eq(6)',tblProductos.row(tr.row).node()).html('$'+compra_diccionario.items.productos[tr.row].subtotal.toFixed(2));
            }
            });
    
    // Evento submit
    $('form').on('submit', function (e) {
        e.preventDefault();
        if(compra_diccionario.items.productos.length === 0){
            message_error('Debe al menos tener un item en su detalle de producto')
            return false;
        }
        if ($('input[name="total"]').val()<=0){
            message_error('El total a pagar debe ser mayor a $0.00')
            return false;
        }
        compra_diccionario.items.fecha = $('input[name="fecha"]').val();
        compra_diccionario.items.proveedor = $('select[name="proveedor"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('descripcion_metodo_pago', $('textarea[name="descripcion_metodo_pago"]').val());
        parameters.append('metodo_pago_valor', document.getElementById('id_metodo_pago').checked);
        parameters.append('compra_diccionario', JSON.stringify(compra_diccionario.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
            alert_action('Notificacion', '¿Desea imprimir la factura de compra?', function () {
                window.open('/App_Facturacion/compra/pdf/'+ response.id +'/', '_blank');
                location.href = '/App_Facturacion/compra/list/';
            }, function () {
                location.href = '/App_Facturacion/compra/list/';
            });
        });
    });

    // Busqueda de productos con select2
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
                    action: 'search_productos',
                    ids: JSON.stringify(compra_diccionario.ids_productos())
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
        data.precio_new = 0.00;
        data.cantidad = 1;
        data.subtotal = 0.00;
        compra_diccionario.add(data);
        $(this).val('').trigger('change.select2');
    });

    compra_diccionario.list();
});
