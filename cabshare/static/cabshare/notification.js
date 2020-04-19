$(function() {
  const notificationSocket = new WebSocket('ws://'+ window.location.host+ '/ws/notification/');

  notificationSocket.onmessage = function(message) {
      var d = JSON.parse(message.data);
      var from_pk = {{user.pk}}
      if(d.to_user == from_pk)
      {
        $("#notifier").append("<i class='fas fa-dot-circle' style='color:red'></i>")
      }
  };

   $("#request").click(function() {
      var data = {
          from_user: $('#from_user_pk').val(),
          to_user: $(this).attr('value'),
          message: "Request to join you on your ride",
      }
      notificationSocket.send(JSON.stringify(data));
      return false;
  });

  html = '<button type="button" class="btn btn-primary" id="cancel" value="'+ data['pk'] +'">Cancel Request</button>'
});
