// Handle QR Code Generation Form Submission
document.addEventListener("DOMContentLoaded", function() {
    const qrForm = document.querySelector(".qr-form");
    const qrInput = document.querySelector(".qr-form input");
    
    qrForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent form from refreshing the page

        const qrData = qrInput.value;
        if (qrData) {
            // Simulate QR code generation process
            alert(`Generating QR code for: ${qrData}`);
            
            // Redirect to a generated QR code page (Replace this with actual logic)
            window.location.href = `/generate/?data=${encodeURIComponent(qrData)}`;
        } else {
            alert("Please enter some data to generate a QR code.");
        }
    });
});

// Rocket Animation (Optional)
window.addEventListener("scroll", function() {
    const rocket = document.querySelector(".rocket");
    const scrollPosition = window.scrollY;

    if (rocket) {
        rocket.style.transform = `translateY(${scrollPosition * 0.2}px)`;
    }
});
