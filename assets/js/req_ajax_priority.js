var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function beforeSendHandler(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
}

$(document).ready(function(){
    $('table').on('click', 'span', function(){
        var path = '';
        var str_priority = '';
        var priority = 0;
        var data = {};
    
        path = $(this).closest("tr").find('.path').text();
        str_priority = $(this).closest("tr").find('.priority').text();
        priority = parseInt(str_priority, 10);
    
        if ($(this).text() == 'Up'){
            priority += 1;
        }else{
            priority = priority > 0 ? priority -= 1 : 0;
        }
        
        data = {
             'path': path,
             'priority': priority
        };
        
        $.ajax({
            url: '/request_ajax/',
            method: 'POST',
            dataType: 'json', 
            data: data,
            beforeSend: beforeSendHandler,
            success: function(data) {
                console.log(data.response);
            },
            error: function (jqXHR, textStatus, errorThrown){
                console.log(jqXHR);
            }
        });
   });
});