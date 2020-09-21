var temp_present_dates = present_dates.sort((a, b) => a - b);
var temp_absent_dates = absent_dates.sort((a, b) => a - b);

$(document).ready(function() {
  var monthNames = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ];
  
  monthNames.forEach((month, index) => {
    let option = document.createElement("option");
    option.innerText = month;
    option.value = index;
    document.querySelector('#select_month').appendChild(option);
  });

  displayDates();
});

function selectMonth(event) {
  if(event.target.value == '') {
    temp_present_dates = present_dates;
    temp_absent_dates = absent_dates;
  } else {
    temp_present_dates = present_dates.filter(item => item.getMonth() == event.target.value);
    temp_absent_dates = absent_dates.filter(item => item.getMonth() == event.target.value);
  }
  displayDates();
}

function displayDates() {
  document.querySelector('#present_dates_container').innerHTML = "";
  document.querySelector('#absent_dates_container').innerHTML = "";
  temp_present_dates.forEach(date => {
    const date_template = document.createElement("div");
    date_template.className = ("col-4 border d-flex justify-content-center align-items-center p-2");
    date_template.innerText = date.toLocaleDateString('en-GB');

    document.querySelector('#present_dates_container').appendChild(date_template);
  });

  temp_absent_dates.forEach(date => {
    const date_template = document.createElement("div");
    date_template.className = ("col-4 border d-flex justify-content-center align-items-center p-2");
    date_template.innerText = date.toLocaleDateString('en-GB');

    document.querySelector('#absent_dates_container').appendChild(date_template);
  });
}