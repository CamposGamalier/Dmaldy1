document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('ticketForm');
    const modal = document.getElementById('modal');
    const verTicketsBtn = document.getElementById('verTicketsBtn');
    const closeButton = document.querySelector('.close-button');
    const ticketsBody = document.getElementById('ticketsBody');
    
    // Variable para almacenar el contador del ID local
    let localTicketIdCounter = 500;

    // Mostrar el modal al hacer clic en el botón "Ver Tickets"
    verTicketsBtn.addEventListener('click', function() {
        modal.style.display = 'block';
        fetchTickets();
    });

    // Cerrar el modal al hacer clic en el botón de cerrar
    closeButton.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Cerrar el modal si se hace clic fuera de él
    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

    // Enviar el formulario al hacer clic en el botón "Enviar Ticket"
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Evita que el formulario se envíe automáticamente
        if (validarFormulario()) {
            guardarDatosLocalmente(obtenerDatosFormulario());
            mostrarMensaje('Ticket guardado localmente.'); // Mensaje de éxito
            limpiarCampos();
            fetchTickets(); // Actualizar la tabla después de agregar un nuevo ticket
        }
    });

    // Función para validar el formulario
    function validarFormulario() {
        const nombreInput = document.getElementById('nombre');
        const correoInput = document.getElementById('correo');
        const descripcionInput = document.getElementById('descripcion');
        
        // Validar nombre
        if (nombreInput.value.length < 4) {
            mostrarMensaje('El nombre debe tener al menos 4 caracteres.');
            return false;
        }
        
        // Validar correo electrónico
        const correoRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!correoRegex.test(correoInput.value)) {
            mostrarMensaje('El correo electrónico ingresado no es válido.');
            return false;
        }
        
        // Validar descripción
        if (descripcionInput.value.length < 10) {
            mostrarMensaje('La descripción debe tener al menos 10 caracteres.');
            return false;
        }

        // Si pasa todas las validaciones, retorna true
        return true;
    }

    // Función para guardar datos del formulario en el almacenamiento local
    function guardarDatosLocalmente(datos) {
        // Incrementar el contador del ID local y asignarlo al nuevo ticket
        datos.id = ++localTicketIdCounter;
        localStorage.setItem('ticketData', JSON.stringify(datos));
    }

    // Función para obtener los datos del formulario
    function obtenerDatosFormulario() {
        const nombreInput = document.getElementById('nombre').value;
        const correoInput = document.getElementById('correo').value;
        const categoriaInput = document.getElementById('categoria').value;
        const descripcionInput = document.getElementById('descripcion').value;
        const imagenInput = document.getElementById('imagen').value; // No se recomienda guardar imágenes en el almacenamiento local
        return {
            nombre: nombreInput,
            correo: correoInput,
            categoria: categoriaInput,
            descripcion: descripcionInput,
            imagen: imagenInput
        };
    }

    // Función para mostrar mensajes al usuario
    function mostrarMensaje(mensaje) {
        const mensajeContainer = document.createElement('div');
        mensajeContainer.classList.add('mensaje-container');
        
        const mensajeElemento = document.createElement('div');
        mensajeElemento.textContent = mensaje;
        mensajeElemento.classList.add('mensaje');
        
        mensajeContainer.appendChild(mensajeElemento);
        document.body.appendChild(mensajeContainer);
        
        setTimeout(() => {
            mensajeContainer.remove();
        }, 3000);
    }

    // Limpiar campos del formulario después de guardar localmente
    function limpiarCampos() {
        form.reset();
    }

    // Función para obtener los datos del formulario guardados localmente
    function obtenerDatosLocalmente() {
        const datos = localStorage.getItem('ticketData');
        return datos ? JSON.parse(datos) : null;
    }

    // Obtener los tickets de la API y mostrarlos en la tabla
    function fetchTickets() {
        fetch('https://jsonplaceholder.typicode.com/comments')
        .then(response => response.json())
        .then(data => {
            // Limpiar el cuerpo de la tabla antes de agregar los nuevos datos
            ticketsBody.innerHTML = '';

            // Agregar cada ticket de la API a la tabla
            data.forEach(ticket => {
                agregarTicketATabla(ticket);
            });

            // Obtener los datos del ticket guardado localmente
            const ticketLocal = obtenerDatosLocalmente();
            if (ticketLocal) {
                // Agregar el ticket guardado localmente a la tabla
                agregarTicketATabla(ticketLocal);
            }
        })
        .catch(error => {
            console.error('Error al obtener los tickets:', error);
        });
    }

    // Función para agregar un ticket a la tabla
    function agregarTicketATabla(ticket) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${ticket.id}</td>
            <td>${ticket.name || ticket.nombre}</td>
            <td>${ticket.email || ticket.correo}</td>
            <td>${ticket.body || ticket.descripcion}</td>
        `;
        ticketsBody.appendChild(row);
    }
});
document.addEventListener("DOMContentLoaded", function() {
    // Obtener el botón de cerrar
    const closeButton = document.getElementById("closeButton");

    // Agregar un evento de clic al botón de cerrar
    closeButton.addEventListener("click", function() {
        // Redirigir a la página de index.html
        window.location.href = "file:///C:/Users/Servidor.OSARCH/Desktop/webprincipal/web/index.html";
    });
});
