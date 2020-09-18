function openNav() {
  document.getElementById("mySidenav").style.width = "300px";
}
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

document.querySelectorAll('[data-row-href]').forEach(item => {
  item.addEventListener("click", function() {
    window.location = this.dataset.rowHref;
  });
});