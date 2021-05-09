var tblClient;
var modal_title;

function get_data() {
    tblClient = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "cliente"},
            {"data": "ciudad"},
            {"data": "c_i"},
            {"data": "ruc"},
            {"data": "estado"},
            {"data": "nombre"},
        ],
        columnDefs: [
            {
                targets: [1],
                render: function (data, type, row) {
                    return '<a href="/App_Facturacion/cliente/show/' + row.id + '/">' + row.cliente + '</a>';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var botones = '<a href="#" rel="edit" title="Editar Cliente" class="btn btn-warning btn-xs btnEdit"><i class="fas fa-edit"></i></a> ';
                    if (row.estado === true) {
                        botones += '<a href="#" rel="delete" title="Eliminar Cliente" class="btn btn-danger btn-xs btnDelete"><i class="fas fa-trash-alt"></i></a> ';
                    }
                    return botones
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var estado = 'Bloqueado'
                    var html = '<span  class="badge badge-warning" >' + estado + '</span>'
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
}

$(function () {
    modal_title = $('.modal-title');
    get_data()
    $('.cerrarModal').on('click', function () {
        limpiarFormModal();
    });
    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de un cliente');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $("#id_estado").attr('checked','True');
        $('#myModalClient').modal('show');
    });

    $('#data tbody')
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html('Edición de un cliente');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblClient.cell($(this).closest('td, li')).index();
            var data = tblClient.row(tr.row).data();
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="ruc"]').val(data.ruc);
            $('input[name="nombre"]').val(data.nombre);
            $('input[name="apellido"]').val(data.apellido);
            $('input[name="ciudad"]').val(data.ciudad);
            $('input[name="direccion"]').val(data.direccion);
            $('input[name="ubicacion"]').val(data.ubicacion);
            $('input[name="ubicacion_link"]').val(data.ubicacion_link);
            $('input[name="c_i"]').val(data.c_i);
            $('input[name="celular"]').val(data.celular);
            $('input[name="correo"]').val(data.correo);
            if (data.estado === true){
                $("#id_estado").attr('checked','True');
            }else {
                 $('#id_estado').removeAttr('checked','False');
            }
            $('#myModalClient').modal('show');
        })
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblClient.cell($(this).closest('td, li')).index();
            var data = tblClient.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el registro Nº'+' <span  class="badge badge-success" > '+ data.id + '</span>' +'?', parameters, function () {
                tblClient.ajax.reload();
            });
        });

    $('form').on('submit', function (e) {
        e.preventDefault();
        filtrar_ubicacion_link()
        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            limpiarFormModal()
            tblClient.ajax.reload();
        });
    });
});

function filtrar_ubicacion_link() {
    var ubicacion = $('input[name="ubicacion"]').val();
    if (ubicacion.length !== 0){
        ubicacion=ubicacion.replace('<iframe src="','');
        ubicacion=ubicacion.replace('" width="600" height="450" frameborder="0" style="border:0;" allowfullscreen="" aria-hidden="false" tabindex="0"><','');
        ubicacion=ubicacion.replace('/iframe>','');
        $('input[name="ubicacion"]').val(ubicacion);
    }
}

//funcion para limpiar el formulario del modal
function limpiarFormModal() {
    $('form')[0].reset();
    $('#myModalClient').modal('hide');
}