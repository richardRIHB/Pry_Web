var tblMarca;
var modal_title;

function get_data() {
    tblMarca = $('#data').DataTable({
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
            {"data": "nombre"},
            {"data": "descripcion"},
            {"data": "estado"},
            {"data": "nombre"},
        ],
        columnDefs: [
            {
                targets: [1],
                render: function (data, type, row) {
                    return '<a href="/App_Facturacion/marca/show/' + row.id + '/">' + row.nombre + '</a>';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" title="Editar Marca" class="btn btn-warning btn-xs btnEdit"><i class="fas fa-edit"></i></a> ';
                    if (row.estado === true) {
                        buttons += '<a href="#" rel="delete" title="Eliminar Marca" class="btn btn-danger btn-xs btnDelete"><i class="fas fa-trash-alt"></i></a> ';
                    }
                    return buttons
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
            {
                targets: [-3],
                render: function (data, type, row) {
                    html = data.substr(0, 70);
                    return html
                }
            },
        ],
        initComplete: function (settings, json) {

        }

    });
};

$(function () {
    modal_title = $('.modal-title');
    get_data();
    //Limpiar el modal al dar click en cerrar
    $('.cerrarModal').on('click', function () {
        limpiarFormModal();
    });
    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de una marca');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $("#id_estado").attr('checked','True');
        $('#myModalMarca').modal('show');
    });

    $('#data tbody')
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html('Edicion de una marca');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblMarca.cell($(this).closest('td, li')).index();
            var data = tblMarca.row(tr.row).data();
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="nombre"]').val(data.nombre);
            $('textarea[name="descripcion"]').val(data.descripcion);
            if (data.estado === true){
                $("#id_estado").attr('checked','True');
            }else {
                 $('#id_estado').removeAttr('checked','False');
            }
            $('#myModalMarca').modal('show');
        })
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblMarca.cell($(this).closest('td, li')).index();
            var data = tblMarca.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el registro Nº'+' <span  class="badge badge-success" > '+ data.id + '</span>' +'?', parameters, function () {
                limpiarFormModal();
                tblMarca.ajax.reload();
            });
        });

    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            limpiarFormModal();
            tblMarca.ajax.reload();
        });
    });
});

//funcion para limpiar el formulario del modal
function limpiarFormModal() {
    $('form')[0].reset();
    $('#myModalMarca').modal('hide');
}
