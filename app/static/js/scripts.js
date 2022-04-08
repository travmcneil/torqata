let spinnerWrapper = document.querySelector('.spinner_wrapper');
let table = document.querySelector('.table');

window.addEventListener('load', function(){
    // setup datatables
    $('#movies_table').DataTable({
        "order": [0, 'desc'],
        "lengthChange": true,
        "bPaginate": true,
            });
    spinnerWrapper.parentElement.removeChild(spinnerWrapper);
    table.style.opacity = 1
    
})