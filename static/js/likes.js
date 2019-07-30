 $(".like").click(function(){ //add event handler to like button
        var eventid; 
        eventid = $(this).attr("data-eventid"); 
        $.get('/whiskyouaway/like/', {event_id: eventid}, function(data){ 
            $('#like_count').html(data); 
                $('#likes').hide();
        }); 
    });
       