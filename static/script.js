(function (){
    var canvas = document.getElementsByTagName('canvas')[0];
    var context = canvas.getContext('2d');
    var width = canvas.width = 800;
    var height = canvas.height = 400;

    var stats = [40, 65, 72, 120, 250, 87, 100, 42];

    context.translate(0, height);
    context.scale(1, -1);

    context.fillStyle = '#f6f6f6';
    context.fillRect(0, 0, width, height);

    var left = 0;
    var prev_stat = stats[0];
    var move_left_by = 100;

    for (stat in stats) {
        the_stat = stats[stat];

        context.beginPath();
        context.moveTo(left, prev_stat);
        context.lineTo(left+move_left_by, the_stat);
        context.lineWidth = 5;
        context.lineCap = 'round';

        /*
        if(the_stat < stats[stat-1]) {
            context.strokeStyle = '#c0392b';
        } else {
            context.strokeStyle = '#3b3b3b';
        }
        */
        context.stroke();

        prev_stat = the_stat;
        left += move_left_by;

    }
})()
