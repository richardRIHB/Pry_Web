function format(d) {
    console.log(d);
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

var tblCuentas;
var modal_title;

function get_data() {
    tblCuentas = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        order: [[ 2, "desc" ]],
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
            {"data": "descripcion"},
            {"data": "valor"},
            {"data": "saldo"},
            {"data": "estado"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [3],
                orderable: false ,
                render: function (data, type, row) {
                    html = data.substr(0, 31);
                    return html
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false ,
                render: function (data, type, row) {
                    var estado = 'Pendiente'
                    var html = '<span  class="badge badge-warning" >' + estado + '</span>'
                    if (row.estado === true && row.estado_venta === true) {
                        estado = 'Pagado'
                        html = '<span  class="badge badge-success" >' + estado + '</span>'
                    }else if(row.estado_venta === false){
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
                    var buttons = '<a href="#" rel="ver" title="Ver Abonos" class="bg bg-success btn-xs  "><i class="fas fa-search"></i>Ver</a> ';
                    buttons += '<a href="/App_Facturacion/cuentas/recibo/' + row.id + '/" title="Imprimir" class="bg bg-dark btn-xs  " target="_blank"><i class="fas fa-print"></i>Imprimir</a> ';

                    if (row.saldo === '0.00'|| row.estado_venta === false) {

                    } else {
                        buttons += '<a  href="#" rel="abonar" title="Abonar" class="bg bg-warning btn-xs  " ><i class="fas fa-edit"></i>Abonar</a> ';
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


    modal_title = $('.modal-title');
    get_data()

    $('#data tbody')
        .on('click', 'a[rel="abonar"]', function () {
            $('input[name="action"]').val('add');
            modal_title.find('span').html('Registrar Abono');
            console.log(modal_title.find('i'));
            modal_title.find('i').removeClass().addClass('fas fa-plus');
            var tr = tblCuentas.cell($(this).closest('td, li')).index();
            var data = tblCuentas.row(tr.row).data();
            $('#lbl_valor').html("Valor: Deuda $" + data.saldo);
            $("input[name='valor']").TouchSpin({
                min: 0,
                max: data.saldo,
                step: 0.01,
                decimals: 2,
                boostat: 5,
                maxboostedstep: 10,
                prefix: 'USD $'
            }).on('change', function () {
                if (isNaN(parseFloat($(this).val()))) {
                    $(this).val(0.00);
                }
            }).val(data.saldo);
            $('#fecha').datetimepicker({
                format: 'DD-MM-YYYY HH:mm A',
                date: moment().format("YYYY-MM-DD HH:mm "),
            });
            $('#span_cuentas').html(data.id);
            $("input[name='cuentas']").val(data.id)
            $('#myModalAbonos').modal('show');
        })
        .on('click', 'a[rel="ver"]', function () {

            var tr = tblCuentas.cell($(this).closest('td, li')).index();
            var datos = tblCuentas.row(tr.row).data();
            console.log(data);

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
                        'id': datos.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "id"},
                    {"data": "fecha"},
                    {"data": "valor"},
                    {"data": "estado"},
                    {"data": "id"},

                ],
                columnDefs: [
                    {
                        targets: [-1],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            var html = ''
                            if (row.estado === true && datos.estado_venta) {
                                html = '<a href="#" rel="anular_abono" type="button" class="btn btn-danger btn-xs"><i class="fas fa-trash-alt"></i>  Anular</a> '
                            }
                            return html;
                        },
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
                ],
                initComplete: function (settings, json) {
                }
            });

            $('#myModelListAbonos').modal('show');
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
        });

    $('#tblDet tbody')
        .on('click', 'a[rel="anular_abono"]', function () {
            var tr = tblAbonos.cell($(this).closest('td, li')).index();
            var data = tblAbonos.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'anular_abono');
            parameters.append('id_abono', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de anular el Abono Nº' +
                ' <span  class="badge badge-success" > ' + data.id + '</span>' + '?', parameters, function () {
                tblAbonos.ajax.reload();
                tblCuentas.ajax.reload();
            });
        });
    $('#myModalAbonos').on('shown.bs.modal', function () {
        //$('form')[0].reset();
    });


    $('form').on('submit', function (e) {
        e.preventDefault();
        var valor = $("input[name='valor']").val();
        if (valor <= 0 ) {
            message_error('Ingrese valor a abonar');
            return false;
        }
        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?',
            parameters, function () {
                $('#myModalAbonos').modal('hide');
                tblCuentas.ajax.reload();
            });
    });
});