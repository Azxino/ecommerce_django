document.addEventListener('DOMContentLoaded', function () {
    const autoAlert = document.querySelectorAll('.alert-dismissible');
    if (autoAlert.length > 0) {
        setTimeout(function () {
            autoAlert.forEach(function (alert) {
                var bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            });
        }, 5000);
    }

    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (el) {
        return new bootstrap.Tooltip(el);
    });

    const confirmForms = document.querySelectorAll(
        '[data-confirm]'
    );
    confirmForms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            if (!confirm(form.dataset.confirm || '¿Estás seguro?')) {
                e.preventDefault();
            }
        });
    });
});
