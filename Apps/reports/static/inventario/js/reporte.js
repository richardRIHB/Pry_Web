var date_now = new moment().format('DD-MM-YYYY');
var produc = null;
var t_filtro_excel = 'Reporte de Inventario'
var produc_excel = '----------------'
var estado_exc = 'Todo'
function generate_report() {
    var parameters = {
        'action': 'search_report',
        'produc': null,
        't_estado':$('select[name="select_estado"]').val()
    };
    if (produc !== null){
        parameters['produc'] = produc
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
                className: 'btn btn-success btn-sm btnTest',
                messageTop: 'PRODUCTO: '+ produc_excel + ', TIPO DE ESTADO: ' + estado_exc,
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
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$'+data
                }
            },
            {
                targets: [-3,-4],
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
    $('<button type="button" class="btn btn-danger btnPDF btn-sm btnTest" title="PDF"><a href="/reports/inventario/pdf/'+$('select[name="select_estado"]').val()+'/'+produc +'/" STYLE="color: white" target="_blank">Descargar Pdf <i class="fas fa-file-pdf"></i></a></button>').appendTo('div.dt-buttons');
}

function formatRepo_produc(repo) {
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
        '<div class="col-lg-2">' +
        '<img src="' + repo.imagen + '" class="img-fluid d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-10 text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.nombre + '(' + repo.descripcion + ')' + '<br>' +
        '<b>Marca:</b> <span class="badge badge-info">' + repo.marca.nombre + '</span>' + '<br>' +
        '<b>Estado:</b> ' + html +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function () {
    $('.btnBorrar').on('click', function () {
        pro = $('select[name="producto"]').val();
        if (pro){
            produc = null;
            produc_excel = '----------------'
            $('select[name="producto"]').val('')
            var elementoProv = document.querySelector("#select2-id_producto-container");
            elementoProv.innerHTML = '<span class="select2-selection__rendered" id="select2-id_producto-container" role="textbox" aria-readonly="true" title="Seleccione"><p class="text-muted">Buscar producto...</p></span>'
            generate_report();
        }
    });
    $('.btnBuscar').on('click', function () {
        produc = $('select[name="producto"]').val();
        if (produc){
            produc_excel = $('select[name="producto"] option:selected').text()
            generate_report();
        }else{
            Swal.fire('Seleccione un producto','','warning')
            return false;
        }
    });

    $('select[name="select_estado"]').on('change', function () {
        produc = $('select[name="producto"]').val();
        estado = $(this).val();
        if (estado === 'btnActivo'){
            estado_exc = 'Activo'
            if (produc){
                produc_excel = $('select[name="producto"] option:selected').text()
                generate_report();
            }else{
                produc_excel = '----------------'
                generate_report()
            }
        }else if(estado === 'btnBloqueado'){
            estado_exc = 'Bloqueado'
            if (produc){
                produc_excel = $('select[name="producto"] option:selected').text()
                generate_report();
            }else{
                produc_excel = '----------------'
                generate_report()
            }
        }else{
            estado_exc = 'Todo'
            if (produc){
                produc_excel = $('select[name="producto"] option:selected').text()
                generate_report();
            }else{
                produc_excel = '----------------'
                generate_report()
            }
        }
    });

    $('select[name="producto"]').on('change', function () {
        produc = $('select[name="producto"]').val();
        if (produc === null){
            produc_excel = '----------------'
            generate_report()
        }
    });
    $('select[name="producto"]').select2({
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
                    action: 'search_producto'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Buscar producto',
        minimumInputLength: 1,
        templateResult: formatRepo_produc,
    });
    generate_report();
})
