$(document).ready(function(){
    
    var current_fs, next_fs, previous_fs; //fieldsets
    var opacity;
    
    var go_next = function(){
        
        //Add Class Active
        $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
        
        //show the next fieldset
        next_fs.show(); 
        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function(now) {
                // for making fielset appear animation
                opacity = 1 - now;
    
                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                });
                next_fs.css({'opacity': opacity});
            }, 
            duration: 600
        });
    };
    
    $(".previous").click(function(){
        
        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();
        
        //Remove class active
        $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
        
        //show the previous fieldset
        previous_fs.show();
    
        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function(now) {
                // for making fielset appear animation
                opacity = 1 - now;
    
                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                });
                previous_fs.css({'opacity': opacity});
            }, 
            duration: 600
        });
    });
    
    $("#account-submit").click(function () {
        let regex = new RegExp('[a-z0-9]+@[a-z]+\.[a-z]{2,3}');
        let email = $("#email");
        let password = $("#password")
        let verify = $("#verify")
        let email_alert = $("#email-alert")
        let password_alert = $("#password-alert")
        let verify_alert = $("#verify-alert")
        if(!regex.test(email.val())){
            email_alert.css('display','block')
            return; 
        }
        email_alert.css('display','None')
        if (password.val()=="") {
            password_alert.css('display','block')
            return;
        }
        password_alert.css('display','None')
        if (password.val()!=verify.val()) {
            verify_alert.css('display','block')
            return;
        }
        password_alert.css('display','None')
        current_fs = $(this).parent();
        next_fs = $(this).parent().next();
        
        go_next();
    })

    $("#coordinate").click(function () {
        navigator.geolocation.getCurrentPosition(fillPosition);
    })
    function fillPosition(position){
        $('#latitude').val(position.coords.latitude)
        $('#longitude').val(position.coords.longitude)
    }

    $('.radio-group .radio').click(function(){
        $(this).parent().find('.radio').removeClass('selected');
        $(this).addClass('selected');
    });
    
    $(".submit").click(function(){
        return false;
    })
        
    });
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))