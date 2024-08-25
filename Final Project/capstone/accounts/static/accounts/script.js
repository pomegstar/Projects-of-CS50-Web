document.addEventListener('DOMContentLoaded', function() {
    const treatmentDateInput = document.getElementById('treatment_date');
    const today = new Date().toISOString().split('T')[0];
    treatmentDateInput.setAttribute('min', today);
});
