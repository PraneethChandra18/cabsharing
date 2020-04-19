$(function() {
  const touserpk = JSON.parse(document.getElementById('to-user-pk').textContent);
  const fromuserpk = JSON.parse(document.getElementById('from-user-pk').textContent);
  const chatSocket = new WebSocket('ws://'+ window.location.host+ '/ws/chat/'+ touserpk + '/');

  chatSocket.onmessage = function(message) {
      var d = JSON.parse(message.data);
      var chat = $("#chat")
      var from_pk = $('#from_user_pk').val()
      var to_pk = $('#to_user_pk').val()
      var html=''
      if(d.from_user == from_pk)
      {
        html = '<div class="row"><div class="col"></div><div class="col" align="right"><div class="card" style="width:50%"><div class="card-body text-left" style="background-color:#3CB371">'
          + d.message + '</div></div></div></div>'
      }
      else {
          html =   '<div class="row"><div class="col"><div class="card" style="width:50%"><div class="card-body text-left" style="background-color:#ADD8E6">'+d.message+
          '</div></div></div><div class="col"></div></div>'

      }

      chat.append(html)
      scrollbottom();
  };

   $("#chatform").on("submit", function(event) {
   var data = {
       from_user: $('#from_user_pk').val(),
       to_user: $('#to_user_pk').val(),
       message: $('#message').val(),
   }
   chatSocket.send(JSON.stringify(data));
   $("#message").val('').focus();
   return false;
  });


  onload = function() {
    document.getElementById("overflow").style.overflow = "auto";
    document.getElementById("bottom").click();
  };

  function scrollbottom(){
  var objDiv = document.getElementById("overflow");
  objDiv.scrollTop = objDiv.scrollHeight;
  }

});
