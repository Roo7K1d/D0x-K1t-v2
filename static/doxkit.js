var button = document.getElementById('toggle-dox');
button.onclick = function (){
  btnDox = document.getElementById("new-dox");
  if (btnDox.style.display === "none"){
    btnDox.style.display = "block";
  }
  else {
    btnDox.style.display = "none";
  }
};
