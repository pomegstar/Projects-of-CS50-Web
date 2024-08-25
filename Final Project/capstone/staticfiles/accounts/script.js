document.addEventListener('DOMContentLoaded', function() {
    let doct = document.querySelector('#doc');
    let pat = document.querySelector('#pat');
    let regidp = document.querySelector('#dp');
    const hospitalO = `
    {% for hos in hospitals %}
        <option  value="{{ hos.id }}">{{ hos }}</option>
    {% endfor %}
    `;
    doct.addEventListener('click', function() {
        regidp.innerHTML = `
    <label>Select hospitals: </label>
    <select class='form-control' name='hospitals' required>
            ${hospitalO}
    </select>
    <label>Specialist at: </label>
    <input class='form-control' type='text' id='specialist' name='specialist' placeholder='Specialist' required>
    <div class="weeks" required>
        <label>Select treatment weeks: </label><br>
        <input type="checkbox" id="week1" name="weeks" value="Sun">
        <label for="task1">Sun </label>
        <input type="checkbox" id="task2" name="weeks" value="Mon">
        <label for="task2">Mon </label>
        <input type="checkbox" id="task3" name="weeks" value="Tue">
        <label for="task3">Tue </label>
        <input type="checkbox" id="task4" name="weeks" value="Wed">
        <label for="task4">Wed </label>
        <input type="checkbox" id="task5" name="weeks" value="Thu">
        <label for="task5">Thu </label>
        <input type="checkbox" id="task1" name="weeks" value="Fri">
        <label for="task1">Fri </label>
        <input type="checkbox" id="task2" name="weeks" value="Sat">
        <label for="task2">Sat </label>
    </div>
    <label>Treatment time: </label><br>
    <label for="from-time">From: </label>
    <input type="time" id="from-time" name="from" required>
    <label for="to-time">To:</label>
    <input type="time" id="to-time" name="to" required><br>
    <input class='btn btn-primary' type='submit' value='Register'>`
    });
    pat.addEventListener('click', function() {
        regidp.innerHTML = `<label>Date of Birth: </label>
    <input class='form-control' type='date' id='birthdate' name= 'birth' required><br>
    <label>Mobile Number: </label>
    <input class='form-control' type='number' placeholder='Number' name='number' min=0 required><br>
    <input class='btn btn-primary' type='submit' value='Register'>`
    })
})
