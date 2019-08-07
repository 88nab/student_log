

$('#likes').click(function(){ var vidid;
vidid = $(this).attr("data-vidid");
$.get('/log/like/', {videoID: vidid}, function(data){
        $('#like_count').html(data);
            $('#likes').hide();
            $('#dislikes').hide();
	}); 
});


$('#dislikes').click(function(){ var vidid;
vidid = $(this).attr("data-vidid");
$.get('/log/dislike/', {videoID: vidid}, function(data){
        $('#dislike_count').html(data);
            $('#dislikes').hide();
            $('#likes').hide();
	}); 
});