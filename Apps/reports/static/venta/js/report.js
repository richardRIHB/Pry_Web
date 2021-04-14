var date_range = null;
var date_now = new moment().format('YYYY-MM-DD');
var fecha_inicio = null;
var fecha_final = null;

function generate_report() {
    var cliente_pk = $('select[name="cliente"]').val();
    var cliente_excel = $('select[name="cliente"] option:selected').text()
    var parameters = {
        'action': 'search_report',
        'start_date': date_now,
        'end_date': date_now,
        'cliente': cliente_pk,
    };
    fecha_inicio = date_now
    fecha_final = date_now
    if (cliente_pk == null){
        cliente_excel = '--------------------';
    }
    if (date_range !== null) {
        parameters['start_date'] = date_range.startDate.format('YYYY-MM-DD');
        parameters['end_date'] = date_range.endDate.format('YYYY-MM-DD');
        fecha_inicio = date_range.startDate.format('YYYY-MM-DD');
        fecha_final = date_range.endDate.format('YYYY-MM-DD');
    }

    $('#data').DataTable({
        lengthMenu: [[20, 30, 45, 50, 100], [20, 30, 45, 50, 100]],
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        order: false,
        paging: true,
        ordering: false,
        info: false,
        searching: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success  ',
                messageTop: 'CLIENTE: '+ cliente_excel,
                messageBottom: 'Fecha: ' + fecha_inicio + ' - ' + fecha_final,
                title: 'Reporte de ventas - ' + date_now,
                customize: function ( xlsx ) {
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('c[r=A1] t', sheet).text( 'TIPO DE REPORTE: ' + 'Reporte de Ventas');
                    $('row c[r^="A"]', sheet).attr( 's', '2' );
                },
            },
        ],
        columnDefs: [
            {
                targets: [-1, -2, -3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
    $('<button type="button" class="btn btn-danger btnPDF" title="PDF"><a href="/reports/venta/pdf/'+ fecha_inicio +'/'+ fecha_final +'/'+ cliente_pk +'/" STYLE="color: white" target="_blank">Descargar Pdf <i class="fas fa-file-pdf"></i></a></button>').appendTo('div.dt-buttons');
}

function formatRepo_cliente(repo) {
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
        '<i class="fas fa-user-tag"></i>' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.cliente + '<br>' +
        '<b>Cedula:</b> ' + repo.c_i + '<br>' +
        '<b>Estado:</b> ' + html +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function () {
    $('input[name="date_range"]').daterangepicker({
        locale: {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-chart-pie"></i> Aplicar',
            cancelLabel: '<i class="fas fa-times"></i> Cancelar',
        }
    }).on('apply.daterangepicker', function (ev, picker) {
        date_range = picker;
        //generate_report();
    }).on('cancel.daterangepicker', function (ev, picker) {
        $(this).data('daterangepicker').setStartDate(date_now);
        $(this).data('daterangepicker').setEndDate(date_now);
        date_range = picker;
        $('select[name="cliente"]').val('');
        var elementoClie = document.querySelector("#select2-id_cliente-container");
        elementoClie.innerHTML = '<span class="select2-selection__rendered" id="select2-id_cliente-container" role="textbox" aria-readonly="true" title="Seleccione"><p class="text-muted">Buscar cliente...</p></span>'
        generate_report();
    });
    $('.btnFecha').on('click', function () {
        $('select[name="cliente"]').val('');
        var elementoClie = document.querySelector("#select2-id_cliente-container");
        elementoClie.innerHTML = '<span class="select2-selection__rendered" id="select2-id_cliente-container" role="textbox" aria-readonly="true" title="Seleccione"><p class="text-muted">Buscar cliente...</p></span>'
        generate_report();
    });

    $('.btnCliente').on('click', function () {
        var provee = $('select[name="cliente"]').val();
        if (provee){
            generate_report();
        } else {
            Swal.fire('Seleccione un cliente','','warning')
            return false;
        }
    });

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
    generate_report();
});