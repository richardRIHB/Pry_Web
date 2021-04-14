var tblProveedor;
var modal_title;
var imag;

function get_data() {
    tblProveedor = $('#data').DataTable({
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
            {"data": "proveedor"},
            {"data": "ciudad"},
            {"data": "empresa"},
            {"data": "ruc"},
            {"data": "estado"},
            {"data": "imagen"},
            {"data": "nombre"},
        ],
        columnDefs: [
            {
                targets: [1],
                render: function (data, type, row) {
                    return '<a href="/App_Facturacion/proveedor/show/' + row.id + '/">' + row.proveedor + '</a>';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" title="Editar Proveedor" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> ';
                    if (row.estado === true) {
                        buttons += '<a href="#" rel="delete" title="Eliminar Proveedor" class="btn btn-danger btn-xs btn-flat btnDelete"><i class="fas fa-trash-alt"></i></a> ';
                    }
                    return buttons
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + row.imagen + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;" >';
                }
            },
            {
                targets: [-3],
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
                targets: [-4],
                orderable: false,
                render: function (data, type, row) {
                    return data
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
        modal_title.find('span').html('Creación de un Proveedor');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $("#id_estado").attr('checked','True');
        $('form')[0].reset();
        $('#myModalProveedor').modal('show');
    });
    $('#data tbody')
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html('Edición de un Proveedor');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblProveedor.cell($(this).closest('td, li')).index();
            var data = tblProveedor.row(tr.row).data();
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="ruc"]').val(data.ruc);
            $('input[name="nombre"]').val(data.nombre);
            $('input[name="apellido"]').val(data.apellido);
            $('input[name="empresa"]').val(data.empresa);
            $('input[name="ciudad"]').val(data.ciudad);
            $('input[name="direccion"]').val(data.direccion);
            $('input[name="c_i"]').val(data.c_i);
            $('input[name="celular"]').val(data.celular);
            $('input[name="correo"]').val(data.correo);
            if (data.estado === true){
                $("#id_estado").attr('checked','True');
            }else {
                 $('#id_estado').removeAttr('checked','False');
            }
            imag = data.imagen
            mostarElemetosFormModal(data.imagen);
            $('#myModalProveedor').modal('show');

        })
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblProveedor.cell($(this).closest('td, li')).index();
            var data = tblProveedor.row(tr.row).data();
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de eliminar el registro Nº'+' <span  class="badge badge-success" > '+ data.id + '</span>' +'?', parameters, function () {
                limpiarFormModal();
                tblProveedor.ajax.reload();
            });
        });

    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        var estado_val = document.getElementById('id_estado').checked;
        parameters.append('estado_valor', estado_val);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            limpiarFormModal();
            tblProveedor.ajax.reload();
        });
    });
});

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

//funcion para limpiar el formulario del modal
function limpiarFormModal() {
    $('form')[0].reset();
    $('#myModalProveedor').modal('hide');
    document.getElementById('visorArchivo').innerHTML =
        '<div> </div>';
}

//funcion para mostrar los datos del select
function mostarElemetosFormModal(ima) {
    //agg informacion
    document.getElementById('visorArchivo').innerHTML =
        '<img src="' + ima + '" alt="Mi imagen" id="miImagen" width="70%" height="200" border=50px>'
}