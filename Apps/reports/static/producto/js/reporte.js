var date_now = new moment().format('DD-MM-YYYY');
var tipo_filtro = null;
var provee = null;
var t_filtro_excel = 'Reporte del Stock de Todos los Productos'
var provee_excel = '----------------'
var linkPDF ='/reports/producto/pdf/'+ tipo_filtro +'/'+ provee +'/'
function generate_report() {
    var parameters = {
        'action': 'search_report',
        'filtro': 'todo_prod',
        'provee': null
    };
    if (tipo_filtro !== null){
        parameters['filtro'] = tipo_filtro
    }
    if (provee !== null){
        parameters['provee'] = provee
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
        info: false,
        searching: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success ',
                messageTop: 'PROVEEDOR: '+ provee_excel,
                messageBottom: 'Fecha de Creación: ' + date_now,
                title: t_filtro_excel + ' ' + date_now,
                customize: function ( xlsx ) {
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('c[r=A1] t', sheet).text( 'TIPO DE REPORTE: '+t_filtro_excel);
                    $('row c[r*="2"]', sheet).attr( 's', '2' );
                    $('row c[r^="A"]', sheet).attr( 's', '2' );
                },
            },
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-2,-3],
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
    $('<button type="button" class="btn btn-danger btnPDF" title="PDF"><a href="'+ linkPDF +'" STYLE="color: white" target="_blank">Descargar Pdf <i class="fas fa-file-pdf"></i></a></button>').appendTo('div.dt-buttons');
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
    $('.btnTodo').on('click', function () {
        tipo_filtro = 'todo_prod';
        provee = null;
        t_filtro_excel = 'Reporte del Stock de Todos los Productos'
        provee_excel = '----------------'
        linkPDF = '/reports/producto/pdf/'+ tipo_filtro +'/'+ provee +'/'
        $('select[name="proveedor"]').val('');
        var elementoProv = document.querySelector("#select2-id_proveedor-container");
        elementoProv.innerHTML = '<span class="select2-selection__rendered" id="select2-id_proveedor-container" role="textbox" aria-readonly="true" title="Seleccione"><p class="text-muted">Buscar proveedor...</p></span>'
        $('select[name="select_filtro"]').val(0)
        generate_report();
    });
    $('.btnMinimo').on('click', function () {
        tipo_filtro = 'minimo_prod';
        provee = null;
        t_filtro_excel = 'Reporte del Stock de los Productos con Existencia Minima'
        provee_excel = '----------------'
        linkPDF = '/reports/producto/pdf/'+ tipo_filtro +'/'+ provee +'/'
        $('select[name="proveedor"]').val('');
        var elementoProv = document.querySelector("#select2-id_proveedor-container");
        elementoProv.innerHTML = '<span class="select2-selection__rendered" id="select2-id_proveedor-container" role="textbox" aria-readonly="true" title="Seleccione"><p class="text-muted">Buscar proveedor...</p></span>'
        $('select[name="select_filtro"]').val(0)
        generate_report();
    });
    $('.btnAgotado').on('click', function () {
        tipo_filtro = 'agotado_prod'
        provee = null;
        t_filtro_excel = 'Reporte del Stock de los Productos Agotados';
        provee_excel = '----------------';
        linkPDF = '/reports/producto/pdf/'+ tipo_filtro +'/'+ provee +'/'
        $('select[name="proveedor"]').val('');
        var elementoProv = document.querySelector("#select2-id_proveedor-container");
        elementoProv.innerHTML = '<span class="select2-selection__rendered" id="select2-id_proveedor-container" role="textbox" aria-readonly="true" title="Seleccione"><p class="text-muted">Buscar proveedor...</p></span>'
        $('select[name="select_filtro"]').val(0)
        generate_report();
    });
    $('select[name="select_filtro"]').on('change', function () {
        provee = $('select[name="proveedor"]').val()
        fil = $('select[name="select_filtro"]').val()
        if (provee || fil === '0'){
            if(fil === 'btnProveeTodo'){
                tipo_filtro = 'todo_prod';
                t_filtro_excel = 'Reporte del Stock de Todos los Productos'
                provee_excel = $('select[name="proveedor"] option:selected').text()
                linkPDF = '/reports/producto/pdf/'+ tipo_filtro +'/'+ provee +'/'
                generate_report();
            }else if(fil === 'btnProveeMinimo') {
                tipo_filtro = 'minimo_prod';
                t_filtro_excel = 'Reporte del Stock de los Productos con Existencia Minima'
                provee_excel = $('select[name="proveedor"] option:selected').text()
                linkPDF = '/reports/producto/pdf/'+ tipo_filtro +'/'+ provee +'/'
                generate_report();
            }else if(fil === 'btnProveeAgotado'){
                tipo_filtro = 'agotado_prod';
                t_filtro_excel = 'Reporte del Stock de los Productos Agotados'
                provee_excel = $('select[name="proveedor"] option:selected').text()
                linkPDF = '/reports/producto/pdf/'+ tipo_filtro +'/'+ provee +'/'
                generate_report();
            }else{
                $('select[name="select_filtro"]').val(0)
            }
        } else {
            Swal.fire('Seleccione un proveedor','','warning')
            $('select[name="select_filtro"]').val(0)
            return false;
        }

    });
    $('select[name="proveedor"]').on('change', function () {
        $('select[name="select_filtro"]').val(0)
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
})
