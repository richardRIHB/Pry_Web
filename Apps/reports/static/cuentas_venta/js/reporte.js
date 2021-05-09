var date_now = new moment().format('DD-MM-YYYY');
var tipo_filtro = 'todo';
var cliente = null;
var t_filtro_excel = 'Reporte de Todas las Cuentas de Venta';
var cliente_excel = '----------------';
function generate_report() {
    var parameters = {
        'action': 'search_report',
        'filtro': 'todo',
        'clien': null
    };
    parameters['filtro'] = tipo_filtro
    if (cliente !== null){
        parameters['clien'] = cliente
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
        ordering: false,
        searching: false,
        info: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-sm btnTest',
                messageTop: 'CLIENTE: '+ cliente_excel,
                messageBottom: 'Fecha de Creación: ' + date_now,
                title: t_filtro_excel + ' ' + date_now,
                customize: function ( xlsx ) {
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('c[r=A1] t', sheet).text( 'TIPO DE REPORTE: '+t_filtro_excel);
                    $('row c[r^="A"]', sheet).attr( 's', '2' );
                },
            },
        ],
        columnDefs: [
            {
                targets: [-1,-2],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                render: function (data, type, row) {
                    return data
                }
            },
            {
                targets: [1,2,3],
                orderable: false,
                render: function (data, type, row) {
                    return data
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
    $('<button type="button" class="btn btn-danger btnPDF btn-sm btnTest" title="PDF"><a href="/reports/cuentas/venta/pdf/'+ tipo_filtro +'/'+ cliente +'/" STYLE="color: white" target="_blank">Descargar Pdf <i class="fas fa-file-pdf"></i></a></button>').appendTo('div.dt-buttons');
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
    $('.btnTodo').on('click', function () {
        tipo_filtro = 'todo';
        cliente = null;
        t_filtro_excel = 'Reporte de Todas las Cuentas de Venta'
        cliente_excel = '----------------'
        $('select[name="cliente"]').val('');
        var elementoProv = document.querySelector("#select2-id_cliente-container");
        elementoProv.innerHTML = '<span class="select2-selection__rendered" id="select2-id_cliente-container" role="textbox" aria-readonly="true" title="Seleccione"><p class="text-muted">Buscar cliente...</p></span>'
        $('select[name="select_filtro"]').val(0)
        generate_report();
    });
    $('.btnValoresPen').on('click', function () {
        tipo_filtro = 'valores_pendientes';
        cliente = null;
        t_filtro_excel = 'Reporte de Cuentas de Venta con Valores Pendientes'
        cliente_excel = '----------------'
        $('select[name="cliente"]').val('');
        var elementoProv = document.querySelector("#select2-id_cliente-container");
        elementoProv.innerHTML = '<span class="select2-selection__rendered" id="select2-id_cliente-container" role="textbox" aria-readonly="true" title="Seleccione"><p class="text-muted">Buscar cliente...</p></span>'
        $('select[name="select_filtro"]').val(0)
        generate_report();
    });
    $('.btnPagado').on('click', function () {
        tipo_filtro = 'pagado'
        cliente = null;
        t_filtro_excel = 'Reporte de Cuentas de Venta con Valores Cancelados';
        cliente_excel = '----------------';
        $('select[name="cliente"]').val('');
        var elementoProv = document.querySelector("#select2-id_cliente-container");
        elementoProv.innerHTML = '<span class="select2-selection__rendered" id="select2-id_cliente-container" role="textbox" aria-readonly="true" title="Seleccione"><p class="text-muted">Buscar cliente...</p></span>'
        $('select[name="select_filtro"]').val(0)
        generate_report();
    });
    $('select[name="select_filtro"]').on('change', function () {
        cliente = $('select[name="cliente"]').val()
        fil = $('select[name="select_filtro"]').val()
        if (cliente || fil === '0'){
            if(fil === 'btnClienteTodo'){
                tipo_filtro = 'todo';
                t_filtro_excel = 'Reporte de Todas las Cuentas de Venta'
                cliente_excel = $('select[name="cliente"] option:selected').text()
                generate_report();
            }else if(fil === 'btnClientePendiente') {
                tipo_filtro = 'valores_pendientes';
                t_filtro_excel = 'Reporte de Cuentas de Venta con Valores Pendientes'
                cliente_excel = $('select[name="cliente"] option:selected').text()
                generate_report();
            }else if(fil === 'btnClientePagado'){
                tipo_filtro = 'pagado';
                t_filtro_excel = 'Reporte de Cuentas de Venta con Valores Cancelados'
                cliente_excel = $('select[name="cliente"] option:selected').text()
                generate_report();
            }else{
                $('select[name="select_filtro"]').val(0)
            }
        } else {
            Swal.fire('Seleccione un cliente','','warning')
            $('select[name="select_filtro"]').val(0)
            return false;
        }

    });
    $('select[name="cliente"]').on('change', function () {
        $('select[name="select_filtro"]').val(0)
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
                    action: 'search_cliente'
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
})
