
function conv_to_lst(str) {
    let rep_str = str.replace(/[\][ ;&#39]/g, '')
    return rep_str.split(',')
}

var num_col = conv_to_lst(num_col);
var cat_col = conv_to_lst(cat_col);


/*function rmv_disabled() {
    let sel_plot = document.getElementById("plot_type").getElementsByTagName("option").value
    $("#plot_type option").prop('disabled', false);

}*/


function rel_valid() {

    document.getElementById('rel-error-p').innerHTML = '';

    let selected_x_col = document.getElementById('x_col').value;
    let selected_y_col = document.getElementById('y_col').value;
    let sel_plot_type = document.getElementById("rel_plot_type");
    /*console.log(selected_x_col)
    console.log(selected_y_col)
    console.log(sel_plot_type.value)*/

    if (selected_x_col == "-1") {
        document.getElementById('rel-error-p').innerHTML = "Please choose column for x-Axis";
        return false;
    }
    else if (selected_y_col == "-1") {
        document.getElementById('rel-error-p').innerHTML = "Please choose column for y-Axis";
        return false;
    }
    else if (sel_plot_type.value == "-1") {
        document.getElementById('rel-error-p').innerHTML = "Please choose plot type";
        return false;
    }

    else if (selected_x_col == selected_y_col) {
        document.getElementById('rel-error-p').innerHTML = "Please choose different variables for Axis";
        return false;
    }

    else if ((cat_col.includes(selected_x_col)) && (cat_col.includes(selected_y_col))) {

        if (sel_plot_type.value != "box") {
            //document.getElementById('sugg-p').innerHTML = 'we recommend to use distribution plots';
            if (confirm('we recommend to use "Individual distribution plots"')) {
                return false;
            };

        }
        else {
            document.getElementById('rel-error-p').innerHTML = "Cannot plot two categorical variables with 'box plot'";
            return false;
        }

    }
    else if ((num_col.includes(selected_x_col)) && (num_col.includes(selected_y_col))) {
        if (sel_plot_type.value != "scatter") {
            //document.getElementById('sugg-p').innerHTML = 'we recommend to use scatter-plot'
            if (confirm('we recommend to use "scatter plot"')) {
                sel_plot_type.value = "scatter";
            }
        }
    }
    else {
        if (sel_plot_type.value == "scatter") {
            //document.getElementById('sugg-p').innerHTML = 'we recommend to use strip-plot'
            if (confirm('we recommend to use "strip plot"')) {
                sel_plot_type.value = "strip";
            }
        }
    }
    return true;
}


function dist_valid() {

    document.getElementById('dist-error-p').innerHTML = '';
    document.getElementById('dist-sugg-p').innerHTML = '';

    let sel_col = document.getElementById('dist_col').value;
    let sel_plot_type = document.getElementById("dist_plot_type");
    /*console.log(selected_x_col)
    console.log(selected_y_col)
    console.log(sel_plot_type.value)*/

    if (sel_col == "-1") {
        document.getElementById('dist-error-p').innerHTML = "Please choose column for Plotting";
        return false;
    }

    else if (sel_plot_type.value == "-1") {
        document.getElementById('dist-error-p').innerHTML = "Please choose plot type";
        return false;
    }

    else if ((cat_col.includes(sel_col)) && (sel_plot_type.value != "count")) {

        document.getElementById('dist-error-p').innerHTML = "Can't plot Categorical data with this plot type";
        document.getElementById('dist-sugg-p').innerHTML = '[ Use Count Plot ]';
        return false;
    }
    else if ((num_col.includes(sel_col)) && (sel_plot_type.value == "count")) {
        //document.getElementById('sugg-p').innerHTML = 'we recommend to use scatter-plot'
        if (confirm('Use other plot type "Count plot may look Clumsy" if column has many unique classes')) {
            return false;
        }
    }
    return true;
}