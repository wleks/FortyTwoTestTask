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
     $('.datepicker').datepicker();
     $('#person-form').validate({
            rules:{
                focusInvalid: false,
                focusCleanup: true,
                name: {
                    required: true,
                    minlength: 3,
                    maxlength: 16
                },
                surname: {
                    required: true,
                    minlength: 3,
                    maxlength: 16
                },
                date_of_birth: {
                    required: true,
                    date: true
                },
                email: {
                    required: true,
                    email: true
                },
                image: {
                    required: false,
                    accept: 'image/*'
                }
            },
            submitHandler: function(form) {
                var $form = $(form);
                var formData = new FormData($('#person-form')[0]);
                var load =  $('#form-loading');
                var message = $('#message');
                $form.find('.form-control').find('input, textarea', 'button').attr('disabled', true);
                $form.attr('class', 'hidden');
                load.html('<img src="/static/712.gif"/>');
                
                $.ajax({
                    url: $(form).attr('action'),
                    type: $(form).attr('method'),
                    data: formData,
                    cache: false,
                    contentType: false,
                    processData: false,
                    beforeSend: beforeSendHandler,
                })
                .done(function(data){
                        var json_data = $.parseJSON(JSON.stringify(data));
                        if (json_data['msg']){
                           $form.find('.form-control').find('input, textarea').attr('disabled', false);
                           $form.find('button').attr('disabled', false);
                           load.html('');
                           message.html('<h3>' + json_data['msg'] + '</h3>');
                           $form.attr('class', 'show');
                           $('.datepicker').focus();
                        } else{
                            $('.errorlist').remove();
                            load.html('');
                            $form.attr('class', 'show');
                            $form.find('.form-control').find('input, textarea', 'button').attr('disabled', false);
                            
                            $.each(json_data, function(i, val) {
                                var id = '#id_' + i;
                                $(id).parent('div').prepend(val);
                            });
                        }
                })
                .fail(function(xhr, str){
                      message.html('<h3>Возникла ошибка: ' + xhr.responseCode + '</h3>');
                });
              
              return false;
            }
              
      });
      //$('#person-form').find('button').attr('disabled', false);
 });