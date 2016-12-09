/**
 * Created by kate on 09.12.16.
 */
$(function() {
    var timerId = 0;
    var $from=$(".from");
    var $to=$(".to");
    var $fun=$(".fun");
    var $graph=$(".graph");
    var $button=$(".button");

    $button.click(function(event) {

        clearInterval( timerId );

        event.preventDefault();
        var from = parseInt($from.val());
        var to = parseInt($to.val());
        var fun = ($fun.val());

        var points = [];
        var dx = 0.05;
        var interval = 10;
        var start = from;
        var end;

        timerId = setInterval( function() {
            end = start + interval;
            if( end > to )
                clearInterval( timerId );
            if( start != from )
                start += 9.9;
            for( ; start < end; start += dx ) {
                if( start > to )
                    break;
                x = start;
                y = eval(fun);
                points.push([x, y]);
            }
            $.plot($graph, [{ label: fun, data: points }], [points], {});
            var i = 0;
            start -= 9.9;
            while( points[i][0] < start ) {
                points.shift();
                i += 1;
            }
        }
        , 100);
    });

});