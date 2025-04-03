document.addEventListener("DOMContentLoaded", function () {
    const sourceSelect = document.getElementById("source");
    const destinationSelect = document.getElementById("destination");
    const qrImage = document.getElementById("qrImage");
    const fareText = document.getElementById("fare");

    // Generate QR code
    window.generateQR = function () {
        let source = sourceSelect.value;
        let destination = destinationSelect.value;

        if (source === destination) {
            alert("Source and destination cannot be the same!");
            return;
        }

        qrImage.src = `/generate_qr?source=${source}&destination=${destination}`;
        fareText.innerText = "Fare will be displayed after scanning.";
    };

    // SocketIO for real-time conductor dashboard updates
    const socket = io.connect("http://127.0.0.1:5002");

    socket.on("update_dashboard", function (ticket_counts) {
        for (let route in ticket_counts) {
            let routeElement = document.getElementById(route);
            if (routeElement) {
                routeElement.innerText = ticket_counts[route];
            }
        }
    });
});
