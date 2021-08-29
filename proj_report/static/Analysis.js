$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip({ 'placement': 'bottom' });    // tooltip 

    //mis_val = mis_val.replace('[]','');
    if (mis_detail.length == 0) {
        document.getElementById('mis_val_lnk').setAttribute("href", "#")        // hide misval info
    }

    $(window).scroll(function () {                      // display btn if scroll >50
        if ($(this).scrollTop() > 80) {
            jQuery('#scroll-up').fadeIn();
        } else {
            jQuery('#scroll-up').fadeOut();
        }
    });
    // scroll body to 0px on click
    $('#scroll-up').click(function () {               // scroll up if clicks
        window.scrollTo({ top: 0, behavior: 'smooth' });
        return false;
    });

});

/* scroll to particular elemant*/
function scroll_to(elemant){
    var scrollDiv = document.getElementById(elemant).offsetTop;
    window.scrollTo({ top: scrollDiv-55, behavior: 'smooth'});
    console.log(elemant);
};

function conv_to_lst(str) {
    let rep_str = str.replace(/[\][ ;&#39]/g, '')
    return rep_str.split(',')
}

var d_f = $('#data-frame').data();
var df_cols = conv_to_lst(df_cols);
var u_col = conv_to_lst(u_col);
var cat_col = conv_to_lst(cat_col);

const Count = arr => arr.reduce((obj, e) => {
    obj[e] = (obj[e] || 0) + 1;     // function it returns unq val as key & count of it as value
    return obj;
}, {});


// Load the Visualization API and the corechart package.
google.charts.load('current', { 'packages': ['corechart'] });

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawChart);

//plot for categorical columns
function drawChart() {
    inde = 0

    for (const i in cat_col) {
        if (u_col.includes(cat_col[i])) {     // no plot for primary key
            continue;
        }
        //console.log(cat_col[i])
        inde = df_cols.indexOf(cat_col[i])
        //console.log(inde)
        data_col = d_f['data'][cat_col[i]];  // extract column values
        //console.log(data_col)
        data_val = Object.keys(data_col).map(function (key) {   // extract values and make into list
            return data_col[key];
        });
        //console.log(data)
        unq_val = [...new Set(data_val)];
        val_count = Count(data_val);     //dict of unq val as key and count as val

        //var fig = document.getElementById("figure_" + inde).getContext("2d");
        //console.log(fig)
        res_val = Object.entries(val_count);
        //console.log(res_val)
        res_val.unshift([i, 'count']);

        var data = google.visualization.arrayToDataTable(
            res_val);

        var options = {
            width: 375,
            height: 250,
            colors: ["#103175"],
            bar: { groupWidth: "70%" },
            legend: { position: 'none' },
            vAxis: {
                textPosition: 'none',       // removes y label
                gridlines: {
                    color: 'transparent'    // removes gridlines
                },
                baselineColor: '#7a7a7a'
            },
            hAxis: {
                textPosition: 'none',
                gridlines: {
                    color: 'transparent'
                },
                baselineColor: '#7a7a7a'
            }
        };

        var chart = new google.visualization.ColumnChart(document.getElementById('figure_' + inde));
        chart.draw(data, options);

        inde++;     // incrementing counter
    }
};


