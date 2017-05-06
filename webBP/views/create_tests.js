function validateForm() {
    var length = parseInt(document.getElementsByName("length")[0].value);
    var streams = parseInt(document.getElementsByName("streams")[0].value);
    var length_range_not_allowed = document.getElementsByName("length_range_not_allowed")[0].value;
    var block_length_range_not_allowed = document.getElementsByName("block_length_range_not_allowed")[0].value;
    var wrong_format = document.getElementsByName("wrong_format")[0].value;
    var checked_any_test = false;
    var error_in = document.getElementsByName("error_in")[0].value;
    if (isNaN(streams))
        streams = 1;

    if (!checkFiles(length, streams)) {
        return false;
    }

    if (document.getElementsByName("frequency")[0].checked) {
        checked_any_test = true;
        if (!checkLengthLessThan(length, 101, 1, error_in, length_range_not_allowed))
            return false;
    }

    if (document.getElementsByName("block_frequency")[0].checked) {
        checked_any_test = true;
        if (!checkBlockLengthInput("block_frequency_param", 2, 20, Math.floor(length / 100), error_in, wrong_format,
            block_length_range_not_allowed))
            return false;

    }

    if (document.getElementsByName("cumulative_sums")[0].checked) {
        checked_any_test = true;
        if (!checkLengthLessThan(length, 101, 3, error_in, length_range_not_allowed))
            return false;
    }

    if (document.getElementsByName("runs")[0].checked) {
        checked_any_test = true;
        if (!checkLengthLessThan(length, 100, 4, error_in, length_range_not_allowed))
            return false;
    }

    if (document.getElementsByName("longest_run_of_ones")[0].checked) {
        checked_any_test = true;
    }

    if (document.getElementsByName("rank")[0].checked) {
        checked_any_test = true;
        if (!checkLengthLessThan(length, 38913, 6, error_in, length_range_not_allowed))
            return false;
    }
    if (document.getElementsByName("discrete_fourier_transform")[0].checked) {
        checked_any_test = true;
        if (!checkLengthLessThan(length, 1000, 7, error_in, length_range_not_allowed))
            return false;
    }

    if (document.getElementsByName("nonperiodic")[0].checked) {
        checked_any_test = true;
    }

    if (document.getElementsByName("overlapping")[0].checked) {
        checked_any_test = true;
        if (!checkBlockLengthInput("overlapping_param", 9, 1, length, error_in, wrong_format,
                block_length_range_not_allowed))
            return false;
    }

    if (document.getElementsByName("universal")[0].checked) {
        checked_any_test = true;
    }

    if (document.getElementsByName("apen")[0].checked) {
        checked_any_test = true;
        var boundary = Math.floor(Math.log(length) / Math.log(2)) - 6;
        if (!checkBlockLengthInput("apen_param", 11, 1, boundary, error_in, wrong_format,
                block_length_range_not_allowed))
            return false;
    }

    if (document.getElementsByName("excursion")[0].checked) {
        checked_any_test = true;
        if (!checkLengthLessThan(length, 1000000, 12, error_in, length_range_not_allowed))
            return false;
    }

    if (document.getElementsByName("excursion_var")[0].checked) {
        checked_any_test = true;
        if (!checkLengthLessThan(length, 1000000, 13, error_in, length_range_not_allowed))
            return false;
    }

    if (document.getElementsByName("serial")[0].checked) {
        checked_any_test = true;
        var boundary = Math.floor(Math.log(length) / Math.log(2)) - 3;
        if (!checkBlockLengthInput("serial_param", 14, 3, boundary, error_in, wrong_format,
                block_length_range_not_allowed))
            return false;
    }

    if (document.getElementsByName("linear")[0].checked) {
        checked_any_test = true;
        if (!checkLengthLessThan(length, 1000001, 15, error_in, length_range_not_allowed))
            return false;
        if (!checkBlockLengthInput("linear_param", 15, 500, 5000, error_in, wrong_format,
                block_length_range_not_allowed))
            return false;
    }

    if (!checked_any_test) {
        alert(document.getElementsByName("no_test_selected")[0].value);
        return false;
    }
    return true;
}

function checkFiles(length, streams) {
    var inputs = document.getElementsByTagName("input");
    var checked_any = false;
    var file_length = 0;
    var length_tag_name = "";
    var name_tag = "";
    var file_name = "";
    for(var i = 0; i < inputs.length; i++) {
        if(inputs[i].name.indexOf('file') == 0) {
            if (inputs[i].checked) {
                if (!checked_any)
                    checked_any = true;
                length_tag_name = "length_".concat(inputs[i].name);
                file_length = parseInt(document.getElementsByName(length_tag_name)[0].value);
                name_tag = "name_".concat(inputs[i].name);
                file_name = document.getElementsByName(name_tag)[0].value;
                if (file_length < length * streams) {
                    var message = document.getElementsByName("length_error")[0].value;
                    message = message.concat(". (", file_name, ")");
                    alert(message);
                    return false;
                }
            }
        }
    }
    if (!checked_any) {
        var message = document.getElementsByName("no_file_selected")[0].value;
        alert(message);
        return false;
    }
    return true;
}

function getTestName(testNum) {
    switch (testNum) {
        case 1:
            return document.getElementsByName("frequency_name")[0].value;
        case 2:
            return document.getElementsByName("block_frequency_name")[0].value;
        case 3:
            return document.getElementsByName("cumulative_sums_name")[0].value;
        case 4:
            return document.getElementsByName("runs_name")[0].value;
        case 5:
            return document.getElementsByName("longest_run_name")[0].value;
        case 6:
            return document.getElementsByName("rank_name")[0].value;
        case 7:
            return document.getElementsByName("discrete_fourier_name")[0].value;
        case 8:
            return document.getElementsByName("nonperiodic_name")[0].value;
        case 9:
            return document.getElementsByName("overlapping_name")[0].value;
        case 10:
            return document.getElementsByName("universal_name")[0].value;
        case 11:
            return document.getElementsByName("approximate_entropy_name")[0].value;
        case 12:
            return document.getElementsByName("random_exc_name")[0].value;
        case 13:
            return document.getElementsByName("random_excs_var_name")[0].value;
        case 14:
            return document.getElementsByName("serial_name")[0].value;
        case 15:
            return document.getElementsByName("linear_complex_name")[0].value;
        default:
            return null;
    }
}

function getDefaultParamValue(testNum) {
    switch (testNum) {
        case 2:
            return 128;
        case 8:
            return 9;
        case 9:
            return 9;
        case 11:
            return 10;
        case 14:
            return 16;
        case 15:
            return 500;
        default:
            return 0;
    }
}

function checkLengthLessThan(length, value, test_num, error_in, length_range_not_allowed) {
    if (length < value) {
        var test_name = getTestName(test_num);
        var res = error_in.concat(" ", test_name, ": ", length_range_not_allowed);
        alert(res);
        return false;
    }
    return true;
}

function checkBlockLengthInput(tag_name , test_num, lower_bound, upper_bound, error_in, wrong_format, block_length_range_not_allowed) {
    var arr = [];
    var param_array = document.getElementsByName(tag_name)[0].value;
    if (param_array.length == 0) {
        var paramValue = getDefaultParamValue(test_num);
        arr = [paramValue];
    }
    else
        arr = param_array.split(',');

    for(var i = 0; i < arr.length; i++) {
        if (isNaN(arr[i])) {
            var test_name = getTestName(test_num);
            var wrong_input = arr[i].trim();
            var res = error_in.concat(" ", test_name, ": ", wrong_format, ". (", wrong_input, ")");
            alert(res);
            return false;
        }

        arr[i] = parseInt(arr[i], 10);

        if ((lower_bound != null && arr[i] < lower_bound) || (upper_bound != null && arr[i] > upper_bound)) {
            var test_name = getTestName(test_num);
            var res = error_in.concat(" ", test_name, ": ", block_length_range_not_allowed, ". (", arr[i], ")");
            alert(res);
            return false;
        }
    }
    return true;
}