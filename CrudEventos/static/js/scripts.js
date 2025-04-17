document.addEventListener("DOMContentLoaded", function () {
  console.log("¡JavaScript cargado con éxito!");
});

function accionActualizar() {
  document.forms[0].submit(); // Envía el primer formulario
}

function accionEliminar() {
  document.forms[1].submit(); // Envía el segundo formulario
}

const formCrear = document.getElementById("formCrear");
const btnCrear = document.getElementById("btnCrear");

 btnCrear.addEventListener("click", function () {
   // Mostramos el cuadro de confirmación
   if (window.confirm("¿Estás seguro de que deseas crear este evento?")) {
     // Si el usuario confirma, enviamos el formulario
     formCrear.submit();
   }
   // Si el usuario cancela, no pasa nada
 });

// Agregue este js para que funcionen los cartelitos de confirmación

