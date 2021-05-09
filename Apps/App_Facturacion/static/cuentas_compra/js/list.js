var tblCuentas;
var tblAbonos;
var modal_title;

function get_data() {
    tblCuentas = $('#data').DataTable({
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
            {"data": "compra.id"},
            {"data": "compra.proveedor.nombre"},
            {"data": "fecha"},
            {"data": "descripcion"},
            {"data": "valor"},
            {"data": "saldo"},
            {"data": "estado"},
            {"data": "estado_compra"},
        ],
        columnDefs: [

            {
                targets: [1],
                orderable: false,
                render: function (data, type, row) {
                    return data.split(' ')[0] + ' ' + row.compra.proveedor.apellido.split(' ')[0];
                }
            },
            {
                targets: [2],
                orderable: false,
                render: function (data, type, row) {
                    return data
                }
            },
            {
                targets: [3],
                orderable: false,
                render: function (data, type, row) {
                    html = data.substr(0, 25);
                    return html
                }
            },
            {
                targets: [-3,-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$'+data
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var estado = 'Pendiente'
                    var html = '<span  class="badge badge-warning" >' + estado + '</span>'
                    if (row.estado === true && row.estado_compra === true) {
                        estado = 'Pagado'
                        html = '<span  class="badge badge-success" >' + estado + '</span>'
                    }else if(row.estado_compra === false){
                        estado = 'Anulado'
                        html = '<span  class="badge badge-danger" >' + estado + '</span>'
                    }
                    return html
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="ver" title="Ver Abonos" class="btn-success btn-xs btn-flat "><i class="fas fa-search"></i> Ver</a> ';
                    buttons += '<a href="/App_Facturacion/cuentas/compra/pdf/' + row.id + '/" class="bg-dark btn-xs" target="_blank"><i class="fas fa-print"></i> Imprimir</a> ';
                    if (row.saldo==='0.00' || row.estado_compra === false){

                    }else {
                        buttons += '<a  href="#" rel="abonar" title="Abonar" class="btn-warning btn-xs btn-flat " ><i class="fas fa-edit"></i> Abonar</a> ';
                    }
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
        }
    });

}

$(function () {
    //Limpiar el modal al dar click en cerrar
    $('.cerrarModal').on('click', function () {
        limpiarFormModal();
    });

    $('input[name="valor"]').on('change', function () {
        var val = $("input[name='valor']").val()
        if(val){

        }else{
           $("input[name='valor']").val(0.00)
       }
    });

    modal_title = $('.modal-title');
    get_data()

    $('#data tbody')
        .on('click', 'a[rel="abonar"]', function () {
            limpiarFormModal();
            $('input[name="action"]').val('add');
            modal_title.find('span').html('Registrar Abono');
            modal_title.find('i').removeClass().addClass('fas fa-plus');
            var tr = tblCuentas.cell($(this).closest('td, li')).index();
            var data = tblCuentas.row(tr.row).data();
            $('input[name="valor"]').trigger("touchspin.updatesettings", {max: data.saldo});
            $('#lbl_valor').html("Valor: Deuda $" + data.saldo);
            $("input[name='valor']").TouchSpin({
                min: 0,
                max: data.saldo,
                step: 0.01,
                decimals: 2,
                boostat: 5,
                maxboostedstep: 10,
                prefix: 'USD $'
            }).val(data.saldo);
            $("input[name='fecha']").val(moment().format("DD/MM/YYYY HH:mm A"));
            $("input[name='cuentas_compra']").val(data.compra.id);
            $("input[name='id']").val(data.id);
            $('#myModalAbonos').modal('show');

        })
        .on('click', 'a[rel="ver"]', function () {
            var tr = tblCuentas.cell($(this).closest('td, li')).index();
            var data = tblCuentas.row(tr.row).data();
           tblAbonos = $('#tblDet').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_abono',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "id"},
                    {"data": "fecha"},
                    {"data": "valor"},
                    {"data": "estado"},
                    {"data": "cuentas_compra"},
                ],
                columnDefs: [
                    {
                        targets: [-1],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            var html = ''
                            if(row.estado === true && row.cuentas_compra.estado === false && row.cuentas_compra.estado_compra === true ){
                              html = '<a href="#" rel="eliminar_abono" class="btn-danger btn-xs"><i class="fas fa-trash-alt"></i> Anular</a> '
                            }
                            return html;
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
                        targets: [-3],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '$'+data
                        }
                    },
                ],
                initComplete: function (settings, json) {
                }
            });

            $('#myModelListAbonos').modal('show');
        })

    $('#tblDet tbody')
        .on('click', 'a[rel="eliminar_abono"]', function () {
            var tr = tblAbonos.cell($(this).closest('td, li')).index();
            var data = tblAbonos.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'delete_abono');
            parameters.append('id_eliminar_abono', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de anular el Abono Nº'+' <span  class="badge badge-success" > '+ data.id + '</span>' +'?', parameters, function () {
                tblAbonos.ajax.reload();
                tblCuentas.ajax.reload();
            });
        });

    $('form').on('submit', function (e) {
        e.preventDefault();
       if($("input[name='valor']").val() <= 0){
            message_error('El valor a ser Abonado debe ser mayor a 0')
            return false;
        }
        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#myModalAbonos').modal('hide');
            tblCuentas.ajax.reload();
        });
    });
});

function limpiarFormModal() {
    $('form')[0].reset();
}
