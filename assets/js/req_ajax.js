var helloRequest = (function($){

  function handleRequest(data) {
    var items = ['<thead><tr><th>Path</th>\
                 <th>Method</th><tr></thead>'];
                 
    var j_data = $.parseJSON(data[1]);
    var id = data[0];
    $.each(j_data, function(i, val) {
        items.push('<tr>'
                    + '<td>' + val.fields.path + '</td>'
                    + '<td>' + val.fields.method + '</td>'
                    + '</tr>'
        );
   });
   var title = $('title').text().split(')')[1] || $('title').text();
   var pre_titile = id ? '(' + id + ') ' : '';
   $('#request').html(items);
   $('title').text(pre_titile + title);
   var str_elem = parseInt(id, 10) + 2;
   $('tr:lt('+str_elem+')').not('tr th').addClass('req');
 }

 return {
     loadRequest: function(){
         $.ajax({
             url: '/request_ajax/',
             dataType : "json",
             success: function(data, textStatus) {
                 handleRequest(data);
             }
         });
     }
 };
})(jQuery);

$(window).on('focus', function() {
    $.ajax({
        url: '/requests/',
        method: 'GET',
        success: function() {
             console.log('requests is viewed');
        }
    });
});

$(document).ready(function(){
    helloRequest.loadRequest();
    setInterval(helloRequest.loadRequest, 500);
});