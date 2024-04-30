function loadFile(event) {
    // get the form
    var form = document.getElementById('form');

    // load csv file
    var csv = event.target.files[0];
    // read csv file
    var reader = new FileReader();
    reader.readAsText(csv);
    reader.onload = function() {
        // split csv file into rows
        var rows = reader.result.split('\n');
        // get the first and second row
        header = rows[0].split(',').slice(2);
        data = rows[1].split(',').slice(2);

        // remove "\r" from the last element
        header[header.length - 1] = header[header.length - 1].replace('\r', '');
        data[data.length - 1] = data[data.length - 1].replace('\r', '');

        // fill the existing form
        for (var i = 0; i < header.length; i++) {
            header[i] = header[i].replace(/"/g, ''); // remove quotes
            if (document.getElementById(header[i])) {
                document.getElementById(header[i]).value = data[i];
            } else {
                console.log('No such element: ' + header[i]);
            }
        }
    
    };
}