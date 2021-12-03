var tblProducts;

function getData(){
    var parameters = {
        'action':'search',
    };

    tblProducts = $('#data').DataTable({
        responsive :true,
        autoWidth: false,
        destroy:true,
        deferRender:true,
        ajax:{
            url:pathname,
            type:'POST',
            headers:{
                'X-CSRFToken':csrftoken
            },
            data:parameters,
            dataSrc: ""
        },
        columns:[
            {data:"code"},
            {data:"name"},
            {data:"category.name"},
            {data:"stock"},
            {data:"pvp"},
            {data:"id"},


        ],
        columnDefs: [
          
       
            {
                targets:[-5],
                class:'text-center',
                render:function(data,type,row){
                    return data;
                }
            },
            {
                targets:[-4],
                class:'text-center',
                render:function(data,type,row){
                    return data
                }
            },
            {
                targets:[-3],
                class:'text-center',
                render:function(data,type,row){
                    return '<span class="badge badge-light">'+row.stock+'</span>';

                }
            },
            {
                targets:[-2],
                class:'text-center',
                render:function(data,type,row){
                    return '$'+ parseFloat(data).toFixed(2);

                }
            },

            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '';
                    buttons += '<a class="btn btn-primary btn-xs btn-flat" rel="serie"><i class="fas fa-folder-open"></i></a> ';
                    return buttons;
                }
            },

          

       
        ],
        rowCallback: function(row,data,index){

        },
        initComplete:function(settings, json){

        }
    });
}
//Informacion del Modal de Detalle de Productos
$(function () {
    getData();

    $('#data tbody')
        .off()
        .on('click', 'a[rel="serie"]', function () {
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
                    
                    {data: "serie"},
                    {data: "sucursal.name"},
                   
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
});