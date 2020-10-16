function scrollToEnd(){
  var chatList = document.getElementById("comments");
  chatList.scrollTop = chatList.scrollHeight;
}
window.onload = scrollToEnd;
