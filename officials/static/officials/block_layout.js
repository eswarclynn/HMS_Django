const letterFloorMap = new Map()
letterFloorMap.set('G', 'Ground');
letterFloorMap.set('F', 'First');
letterFloorMap.set('S', 'Second');
letterFloorMap.set('T', 'Third');
letterFloorMap.set('Fo', 'Fourth');

window.onload = function() {
  var filled_count = 0;
  var partial_count = 0;
  var vacant_count = 0;

  document.querySelectorAll('.room-card').forEach((room_card) => {
    let room_str = room_card.innerHTML;
    let [floor, no] = room_str.split("-");
    no = parseInt(no);
    floor = letterFloorMap.get(floor);
    let room_students = roomdetails.filter(room => room.floor == floor && room.room_no == no);
    let count = room_students.length || 0;
    if (count == room_capacity) {
      filled_count += 1;
      room_card.classList.add('filled');
    } else if (0 < count && count < room_capacity) {
      room_card.classList.add("partial");
      partial_count += 1;
    } else if (count == 0) {
      vacant_count += 1;
    }

    $(room_card).hover(() => {
      const room_regd_nos = room_students.map(stud => stud.student.regd_no).join(", ");
      if (room_regd_nos.length > 0) {
        $(room_card).tooltip({title: room_regd_nos}).tooltip('show');
      }
    });

    const table = document.getElementById("table-container");
    room_card.addEventListener('click', function() {
      placeDetails(room_str, floor, no, room_students);
      if (table.classList.contains('d-none')) {
        table.classList.add('d-block');
        table.classList.remove('d-none');
      }  
      document.querySelector('#table-container table > tbody').scrollIntoView();
    });
  });

  document.getElementById('filled_room').innerHTML = filled_count;
  document.getElementById('partial_room').innerHTML = partial_count;
  document.getElementById('vacant_room').innerHTML = vacant_count;

  document.getElementById('ground-con').style.display = "block";
}

function closeRoomTable() {
  table = document.getElementById("table-container");
  if (table.classList.contains('d-block')) {
    table.classList.remove('d-block');
    table.classList.add('d-none');
  }
}

function showFloor() {
  const floor = document.getElementById("floor").value.toLowerCase();
  const floor_id = floor+"-con";
  document.querySelectorAll(".floor-con").forEach(floor_con => floor_con.style.display = "none");
  document.getElementById(floor_id).style.display = "block";
}

function placeDetails(room_str, floor, no, room_students) {
  document.querySelector('#table-container h2#room').innerHTML = room_str;
  let tbody = document.querySelector('#table-container table > tbody');
  tbody.innerHTML = "";
  room_students.forEach(room => {
    let row = document.createElement('tr');
    row.innerHTML = `
      <td>${room.student.regd_no}</td>\
      <td>${room.student.roll_no}</td>\
      <td>${room.student.name}</td>\
      <td>${room.student.year}</td>\
      <td>${room.student.branch}</td>\
      <td>${room.student.phone}</td>\
      <td>${room.student.email}</td>\
      <td>\
        <form method="POST" onsubmit="return confirm('Are you sure?')">
          <input type="hidden" name="roomdetail_id" value="${room.id}" />
          <input type='submit' name='remove' value='Remove' class='btn btn-danger' />\
        </form>
      </td>`;
    tbody.appendChild(row);
  })

  if (room_students.length < room_capacity) {
    let row = document.createElement('tr');
    row.innerHTML = `
      <td colspan='10' class='text-center'>\
        <form method="POST">
          Add Student to room :\
          <input type='text' name='regd_no' class='ml-4'> \
          <input type='hidden' name='block_id' value='${current_block.id}' /> \
          <input type='hidden' name='floor' value='${floor}' /> \
          <input type='hidden' name='room_no' value='${no}' /> \
          <input type='submit' name='Add' value='Add' class='btn btn-primary ml-5'>\
        </form>
      </td>`;
    tbody.appendChild(row); 
  }
}
