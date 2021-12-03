var tblProducts;

function getData() {
    var parameters = {
        'action': 'search',
    };

    tblProducts = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: pathname,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: parameters,
            dataSrc: ""
        },
        columns: [
            {data: "id"},
            {data: "name"},
            {data: "category.name"},
            {data: "stock_minimum"},
            {data: "stock_maximum"},
            {data: "image"},
            {data: "price"},
            {data: "pvp"},
            {data: "price_promotion"},
            {data: "stock"},
            {data: "id"},
        ],
        columnDefs: [
            {
                targets: [-7, -8],
                class: 'text-center',
                render: function (data, type, row) {
                    return data;
                }
            },
            {
                targets: [-6],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<img alt="" src="' + row.image + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                }
            },
            {
                targets: [-4, -5, -3],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    if (row.category.inventoried) {
                        if (row.stock > 0) {
                            return '<a rel="series" class="btn btn-success btn-xs">' + row.stock + '</a>';
                        }
                        return '<span class="badge badge-danger">' + row.stock + '</span>';
                    }
                    return '<span class="badge badge-secondary">Sin stock</span>';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '';
                    buttons += '<a href="/pos/scm/product/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/pos/scm/product/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a> ';
                    return buttons;
                }
            },
        ],
        rowCallback: function (row, data, index) {

        },
        initComplete: function (settings, json) {

        }
    });
}
//Informacion del Modal de Detalle de Productos
$(function () {
    getData();

    $('#data tbody')
        .off()
        .on('click', 'a[rel="series"]', function () {
            $('.tooltip').remove();
            var tr = tblProducts.cell($(this).closest('td, li')).index(),
                row = tblProducts.row(tr.row).data();
            $('#tblSeries').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                info: false,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_series',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "date_joined"},
                    {data: "purchase.id"},
                    {data: "sucursal.name"},
                    {data: "serie"},
                ],
                columnDefs: [
                    {
                        targets: ['_all'],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ]
            });
            $('#myModalSeries').modal('show');
        });
})