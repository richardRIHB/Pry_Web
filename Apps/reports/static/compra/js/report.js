var date_range = null;
var date_now = new moment().format('YYYY-MM-DD');
var fecha_inicio = null;
var fecha_final = null;

function generate_report() {
    var provee_pk = $('select[name="proveedor"]').val();
    var provee_excel = $('select[name="proveedor"] option:selected').text()
    var parameters = {
        'action': 'search_report',
        'start_date': date_now,
        'end_date': date_now,
        'proveedor': provee_pk,
    };
    fecha_inicio = date_now
    fecha_final = date_now
    if (provee_pk == null){
        provee_excel = '--------------------';
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
                messageTop: 'PROVEEDOR: '+ provee_excel,
                messageBottom: 'Fecha: ' + fecha_inicio + ' - ' + fecha_final,
                title: 'Reporte de compras - ' + date_now,
                customize: function ( xlsx ) {
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('c[r=A1] t', sheet).text( 'TIPO DE REPORTE: ' + 'Reporte de Compras');
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
    $('<button type="button" class="btn btn-danger btnPDF" title="PDF"><a href="/reports/compra/pdf/'+ fecha_inicio +'/'+ fecha_final +'/'+ provee_pk +'/" STYLE="color: white" target="_blank">Descargar Pdf <i class="fas fa-file-pdf"></i></a></button>').appendTo('div.dt-buttons');
}

function formatRepo_proveedor(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var html = '<span  class="badge badge-success" >' + repo.empresa + '</span>'

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
        '<b>Cedula:</b> ' + repo.c_i + '<br>' +
        '<b>Empresa:</b> ' + html +
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
        $('select[name="proveedor"]').val('');
        var elementoProv = document.querySelector("#select2-id_proveedor-container");
        elementoProv.innerHTML = '<span class="select2-selection__rendered" id="select2-id_proveedor-container" role="textbox" aria-readonly="true" title="Seleccione"><p class="text-muted">Buscar proveedor...</p></span>'
        generate_report();
    });
    $('.btnFecha').on('click', function () {
        $('select[name="proveedor"]').val('');
        var elementoProv = document.querySelector("#select2-id_proveedor-container");
        elementoProv.innerHTML = '<span class="select2-selection__rendered" id="select2-id_proveedor-container" role="textbox" aria-readonly="true" title="Seleccione"><p class="text-muted">Buscar proveedor...</p></span>'
        generate_report();
    });

    $('.btnProveedor').on('click', function () {
        var provee = $('select[name="proveedor"]').val();
        if (provee){
            generate_report();
        } else {
            Swal.fire('Seleccione un proveedor','','warning')
            return false;
        }
    });

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
    generate_report();
});