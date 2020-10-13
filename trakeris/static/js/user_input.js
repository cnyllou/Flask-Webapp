
function listen_input() {
  // Declare variables
 var input, filter, container, item, name, i, txtValue;
 input = document.getElementById('user_input');
 filter = input.value.toUpperCase();
 container = document.getElementById("container");
 item = container.getElementsByClassName('catalog-item');


 // Loop through all list items, and hide those who don't match the search query
for (i = 0; i < item.length; i++) {
  name = item[i].getElementsByClassName("item-name")[0];
  txtValue = name.textContent || name.innerText;

  if (txtValue.toUpperCase().indexOf(filter) > -1){
    item[i].style.display = "";
  } else {
    item[i].style.display = "none";
  }
 }
}
