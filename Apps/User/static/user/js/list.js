var tblUsuario;
var modal_title;
var imag;

function get_data() {
    tblUsuario = $('#data').DataTable({
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
            {"data": "first_name"},
            {"data": "last_name"},
            {"data": "username"},
            {"data": "date_joined"},
            {"data": "is_active"},
            {"data": "imagen"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [1],
                class: 'text-center',
                render: function (data, type, row) {
                    return data
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" title="Editar Usuario" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> ';
                    if (row.is_active === true){
                        buttons += '<a href="#" rel="delete" title="Eliminar Usuario" class="btn btn-danger btn-xs btn-flat btnDelete"><i class="fas fa-trash-alt"></i></a> ';
                    }
                    return buttons
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="'+ data +'" class="img-fluid mx-auto d-block" style="width: 20px; height: 20px;">';
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var estado = 'Bloqueado'
                    var html = '<span  class="badge badge-warning" >' + estado + '</span>'
                    if (row.is_active === true) {
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
    get_data();
    //Limpiar el modal al dar click en cerrar
    $('.cerrarModal').on('click', function () {
        limpiarFormModal();
    });
    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de un usuario');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $("#id_is_active").attr('checked','True');
        $('#myModalUsuario').modal('show');
    });

    $('#data tbody')
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html('Edicion de un usuario');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblUsuario.cell($(this).closest('td, li')).index();
            var data = tblUsuario.row(tr.row).data();
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="username"]').val(data.username);
            $('input[name="first_name"]').val(data.first_name);
            $('input[name="last_name"]').val(data.last_name);
            $('input[name="email"]').val(data.email);
            $('input[name="password"]').val(data.password);
            if (data.is_active === true){
                $("#id_is_active").attr('checked','True');
            }else {
                 $('#id_is_active').removeAttr('checked','False');
            }
            imag = data.imagen
            mostarElemetosFormModal(data.imagen);
            $('#myModalUsuario').modal('show');
        })
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblUsuario.cell($(this).closest('td, li')).index();
            var data = tblUsuario.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar al Usuario Nº'+' <span  class="badge badge-success" > '+ data.id + '</span>' +'?', parameters, function () {
                limpiarFormModal();
                tblUsuario.ajax.reload();
            });
        });

    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            limpiarFormModal();
            tblUsuario.ajax.reload();
        });
    });
});

//funcion para limpiar el formulario del modal
function limpiarFormModal() {
    $('form')[0].reset();
    $('#myModalUsuario').modal('hide');
    document.getElementById('visorArchivo').innerHTML =
        '<div> </div>';
}

//acciones secundarias para activar otras acciones
$(document).ready(function () {
    $(document).on("click", "#btn_id", function () {
        $("#id_imagen").click();
    })

})

function validarInputFile() {
    var archivoInput = document.getElementById('id_imagen');
    var accion = $('input[name="action"]').val()
    var archivoRuta = archivoInput.value;
    var extencionesPermitidas = /(.png|.PNG|.jpg|.jpeg)$/i;

    if (!extencionesPermitidas.exec(archivoRuta)) {
        Swal.fire({
            title: 'Error!',
            text: 'Asegúrate de haber seleccionado una imagen.',
            icon: 'error'
        });
        archivoInput.value = '';
        if (accion === 'edit'){
            document.getElementById('visorArchivo').innerHTML =
                '<img src="' + imag + '" alt="Mi imagen" id="miImagen" width="70%" height="200" border=50px>'
        }else{
            document.getElementById('visorArchivo').innerHTML =
                '<div> </div>';
        }
        return false;
    } else {
        if (archivoInput.files && archivoInput.files[0]) {
            var visor = new FileReader();
            visor.onload = function (e) {
                document.getElementById('visorArchivo').innerHTML =
                    '<img src="' + e.target.result + '" alt="Mi imagen" id="miImagen" width="70%" height="200" border=50px>';
            };
            visor.readAsDataURL(archivoInput.files[0]);
        }
    }
}

//funcion para mostrar datos restantes en el modal
function mostarElemetosFormModal(ima) {
    //agg informacion
    document.getElementById('visorArchivo').innerHTML =
        '<img src="' + ima + '" alt="Mi imagen" id="miImagen" width="70%" height="200" border=50px>'
}