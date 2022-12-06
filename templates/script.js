function add_child(){
    const fs = require('fs');
    fs.readFile('runtime.txt', 'utf-8',(err, data) => {
        if (err) {
            console.error(err);
            return;
        }
        document.getElementById('baka').innerHTML = data;
    });
}