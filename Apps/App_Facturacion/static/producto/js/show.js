var div_miniaturas = document.getElementById('miniaturas');
var fotos = div_miniaturas.getElementsByTagName('img');

for( var i = 0; i < fotos.length; i++ ){
    var que_imagen = fotos[i];
        que_imagen.onclick = function () {
            if (document.getElementById('activo')){
                document.getElementById('activo').id = '';
            }
            var imagen_grande = document.getElementById('big').getElementsByTagName('img')[0];
            var source = this.src;
            this.id = 'activo';
            imagen_grande.src = source;
        }
}
