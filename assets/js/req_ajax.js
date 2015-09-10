var helloRequest = (function($){

  function handleRequest(data) {
    var items = [];
    var j_data = $.parseJSON(data[1]);
    
    j_data.sort(function(a, b){
        var a1= a.fields.priority, b1= b.fields.priority;
        if(a1 == b1) return 0;
            return a1< b1? 1: -1;
    });
    var id = data[0];
    $.each(j_data, function(i, val) {
        items.push('<tr>'
           + '<td class="path">' + val.fields.path + '</td>'
           + '<td>' + val.fields.method + '</td>'
           + '<td class="priority">' + val.fields.priority + '</td>'
           + '<td><a href="#!"><span class="glyphicon glyphicon-arrow-up" aria-hidden="true">Up</span></a></td>'
           + '<td><a href="#!"><span class="glyphicon glyphicon-arrow-down" aria-hidden="true">Down</span></a></td>'
           + '</tr>'
        );
    });
    
    $('#request tbody').html(items);
    
    var title = $('title').text().split(')')[1] || $('title').text();
    var pre_titile = id ? '(' + id + ') ' : '';
    $('title').text(pre_titile + title);
    
    var str_elem = parseInt(id, 10) + 1;
    $('tr:lt(' + str_elem + ')').not('tr th').addClass('req');
    
    $('td').addClass('text-center');
    $('th').addClass('text-center');
  }
  return {
     loadRequest: function(){
         $.ajax({
             url: '/request_ajax/',
             method: 'GET',
             dataType : "json",
             success: function(data, textStatus) {
                 handleRequest(data);
             }
         });
     }
  };
})(jQuery);

$(document).ready(function(){
    helloRequest.loadRequest();
    setInterval(helloRequest.loadRequest, 500);
    $(window).on('focus', function() {
        $.ajax({
            url: '/requests/',
            method: 'GET',
            success: function() {
                console.log('requests is viewed');
            }
        });
    });
});