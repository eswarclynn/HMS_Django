// Sidenav methods
function openNav() {
  document.getElementById("mySidenav").style.width = "300px";
}
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

// Toasts from Django messages
toast_messages.forEach(item => {
  if(item.tag == 'success') {
    iziToast.success({
      message: item.message,
      position: 'topRight'
    });
  }
  if(item.tag == 'error') {
    iziToast.error({
      message: item.message,
      position: 'topRight'
    });
  }
  if(item.tag == 'warning') {
    iziToast.warning({
      message: item.message,
      position: 'topRight'
    });
  }
  if(item.tag == 'info') {
    iziToast.info({
      message: item.message,
      position: 'topRight'
    });
  }
})

document.querySelectorAll('[data-row-href]').forEach(item => {
  item.style.cursor = "pointer";

  item.querySelectorAll("button").forEach(item => {
    item.addEventListener("click", event => {
      event.stopPropagation();
    });
  });

  item.querySelectorAll("input").forEach(item => {
    item.addEventListener("click", event => {
      event.stopPropagation();
    });
  });
  
  item.querySelectorAll("a").forEach(item => {
    item.addEventListener("click", event => {
      event.stopPropagation();
    })
  });

  item.addEventListener("click", function() {
    window.location = this.dataset.rowHref;
  });
});