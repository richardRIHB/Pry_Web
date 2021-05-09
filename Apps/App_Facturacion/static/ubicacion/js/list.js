var tblBloque;
var tblSeccion;
var tblPosicion;
var tblArea;
var modal_title;

function get_data_Boque() {
    tblBloque = $('#data').DataTable({
        lengthMenu: [[5, 10, 25, 50, 100], [5, 10, 25, 50, 100]],
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchBloque',
                'modulo': 'nada'
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
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" title="Editar Bloque" class="btn btn-warning btn-xs btnEdit"><i class="fas fa-edit"></i></a> ';
                    if (row.estado === true) {
                        buttons += '<a href="#" rel="delete" title="Eliminar Bloque" class="btn btn-danger btn-xs btnDelete"><i class="fas fa-trash-alt"></i></a> ';
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
        ],
        initComplete: function (settings, json) {

        }

    });
};

function get_data_Seccion() {
    tblSeccion = $('#data_Seccion').DataTable({
        lengthMenu: [[5, 10, 25, 50, 100], [5, 10, 25, 50, 100]],
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchSeccion',
                'modulo': 'nada'
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
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" title="Editar Seccion" class="btn btn-warning btn-xs btnEdit"><i class="fas fa-edit"></i></a> ';
                    if (row.estado === true) {
                        buttons += '<a href="#" rel="delete" title="Eliminar Seccion" class="btn btn-danger btn-xs btnDelete"><i class="fas fa-trash-alt"></i></a> ';
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
        ],
        initComplete: function (settings, json) {

        }

    });
};

function get_data_Posicion() {
    tblPosicion = $('#data_Posicion').DataTable({
        lengthMenu: [[5, 10, 25, 50, 100], [5, 10, 25, 50, 100]],
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchPosicion',
                'modulo': 'nada'
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
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" title="Editar Posicion" class="btn btn-warning btn-xs btnEdit"><i class="fas fa-edit"></i></a> ';
                    if (row.estado === true) {
                        buttons += '<a href="#" rel="delete" title="Eliminar Posicion" class="btn btn-danger btn-xs btnDelete"><i class="fas fa-trash-alt"></i></a> ';
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
        ],
        initComplete: function (settings, json) {

        }

    });
};

$(function () {
    modal_title = $('.modal-title');
    get_data_Boque();
    get_data_Seccion();
    get_data_Posicion();
    //Limpiar el modal al dar click en cerrar
    $('.cerrarModal').on('click', function () {
        limpiarFormModal();
    });
    $('.btnAddBloque').on('click', function () {
        $('input[name="modulo"]').val('moduloBloque');
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de un Bloque');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $("#id_estado").attr('checked','True');
        $('#myModal').modal('show');
    });
    $('.btnAddSeccion').on('click', function () {
        $('input[name="modulo"]').val('moduloSeccion');
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de una Sección');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $("#id_estado").attr('checked','True');
        $('#myModal').modal('show');
    });
    $('.btnAddPosicion').on('click', function () {
        $('input[name="modulo"]').val('moduloPosicion');
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de una Posición');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $("#id_estado").attr('checked','True');
        $('#myModal').modal('show');
    });

    $('#data tbody')
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html('Edición de un Bloque');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblBloque.cell($(this).closest('td, li')).index();
            var data = tblBloque.row(tr.row).data();
            $('input[name="modulo"]').val('moduloBloque');
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="nombre"]').val(data.nombre);
            $('textarea[name="descripcion"]').val(data.descripcion);
            if (data.estado === true){
                $("#id_estado").attr('checked','True');
            }else {
                 $('#id_estado').removeAttr('checked','False');
            }
            $('#myModal').modal('show');
        })
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblBloque.cell($(this).closest('td, li')).index();
            var data = tblBloque.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('modulo', 'moduloBloque');
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el registro Nº'+' <span  class="badge badge-success" > '+ data.id + '</span>' +'?', parameters, function () {
                tblBloque.ajax.reload();
            });
        });

    $('#data_Seccion tbody')
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html('Edición de una Sección');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblSeccion.cell($(this).closest('td, li')).index();
            var data = tblSeccion.row(tr.row).data();
            $('input[name="modulo"]').val('moduloSeccion');
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="nombre"]').val(data.nombre);
            $('textarea[name="descripcion"]').val(data.descripcion);
            if (data.estado === true){
                $("#id_estado").attr('checked','True');
            }else {
                 $('#id_estado').removeAttr('checked','False');
            }
            $('#myModal').modal('show');
        })
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblSeccion.cell($(this).closest('td, li')).index();
            var data = tblSeccion.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('modulo', 'moduloSeccion');
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el registro Nº'+' <span  class="badge badge-success" > '+ data.id + '</span>' +'?', parameters, function () {
                tblSeccion.ajax.reload();
            });
        });

    $('#data_Posicion tbody')
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html('Edición de una Posición');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblPosicion.cell($(this).closest('td, li')).index();
            var data = tblPosicion.row(tr.row).data();
            $('input[name="modulo"]').val('moduloPosicion');
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="nombre"]').val(data.nombre);
            $('textarea[name="descripcion"]').val(data.descripcion);
            if (data.estado === true){
                $("#id_estado").attr('checked','True');
            }else {
                 $('#id_estado').removeAttr('checked','False');
            }
            $('#myModal').modal('show');
        })
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblPosicion.cell($(this).closest('td, li')).index();
            var data = tblPosicion.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('modulo', 'moduloPosicion');
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el registro Nº'+' <span  class="badge badge-success" > '+ data.id + '</span>' +'?', parameters, function () {
                tblPosicion.ajax.reload();
            });
        });

    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        var estado_val = document.getElementById('id_estado').checked;
        parameters.append('estado_valor', estado_val);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            limpiarFormModal();
            tblBloque.ajax.reload();
            tblSeccion.ajax.reload();
            tblPosicion.ajax.reload();
        });
    });
});

//funcion para limpiar el formulario del modal
function limpiarFormModal() {
    $('form')[0].reset();
    $('#myModal').modal('hide');
}

function mostrar_bloque() {
    document.getElementById('contenido_1').style.display = 'block';
    document.getElementById('contenido_2').style.display = 'none';
    document.getElementById('contenido_3').style.display = 'none';
}

function mostrar_seccion() {

    document.getElementById('contenido_2').style.display = 'block';
    document.getElementById('contenido_3').style.display = 'none';
    document.getElementById('contenido_1').style.display = 'none';
}

function mostrar_posicion() {
    document.getElementById('contenido_3').style.display = 'block';
    document.getElementById('contenido_2').style.display = 'none';
    document.getElementById('contenido_1').style.display = 'none';
}