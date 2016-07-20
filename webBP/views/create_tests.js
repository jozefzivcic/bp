function validateForm() {
    var length = parseInt(document.getElementsByName("length")[0].value);
    var streams = parseInt(document.getElementsByName("streams")[0].value);
    var test = document.getElementsByName("test")[0].value;
    var length_range_not_allowed = document.getElementsByName("length_range_not_allowed")[0].value;
    var block_length_range_not_allowed = document.getElementsByName("block_length_range_not_allowed")[0].value;
    var wrong_format = document.getElementsByName("wrong_format")[0].value;
    var checked_any_test = false;
    if (isNaN(streams))
        streams = 1;

    if (!checkFiles(length, streams)) {
        return false;
    }

    if (document.getElementsByName("frequency")[0].checked) {
        checked_any_test = true;
        if (length <= 100) {
            var res = test.concat(" 1. ", length_range_not_allowed);
            alert(res);
            return false;
        }
    }

    if (document.getElementsByName("block_frequency")[0].checked) {
        checked_any_test = true;
        var param_array = document.getElementsByName("linear_param")[0].value;
        if (param_array.length == 0)
            return true;
        for(var i=0; i<arr.length; i++) {
            if (isNaN(arr[i])) {
                var res = test.concat(" 2. ", wrong_format, ". (", arr[i], ")");
                alert(res);
                return false;
            }
            arr[i] = parseInt(arr[i], 10);

            if (arr[i] < 20 || arr[i] > Math.floor(length / 100)) {
                var res = test.concat(" 2. ", block_length_range_not_allowed, ". (", arr[i], ")");
                alert(res);
                return false;
            }
        }
    }

    if (document.getElementsByName("cumulative_sums")[0].checked) {
        checked_any_test = true;
        if (length <= 100) {
            var res = test.concat(" 3. ", length_range_not_allowed);
            alert(res);
            return false;
        }
    }

    if (document.getElementsByName("runs")[0].checked) {
        checked_any_test = true;
        if (length < 100) {
            var res = test.concat(" 4. ", length_range_not_allowed);
            alert(res);
            return false;
        }
    }

    if (document.getElementsByName("longest_run_of_ones")[0].checked) {
        checked_any_test = true;
    }

    if (document.getElementsByName("rank")[0].checked) {
        checked_any_test = true;
        if (length <= 38912) {
            var res = test.concat(" 6. ", length_range_not_allowed);
            alert(res);
            return false;
        }
    }
    if (document.getElementsByName("discrete_fourier_transform")[0].checked) {
        checked_any_test = true;
        if (length < 1000) {
            var res = test.concat(" 7. ", length_range_not_allowed);
            alert(res);
            return false;
        }
    }

    if (document.getElementsByName("nonperiodic")[0].checked) {
        checked_any_test = true;
    }

    if (document.getElementsByName("overlapping")[0].checked) {
        checked_any_test = true;
        var param_array = document.getElementsByName("linear_param")[0].value;
        if (param_array.length == 0)
            return true;
        for(var i=0; i<arr.length; i++) {
            if (isNaN(arr[i])) {
                var res = test.concat(" 2. ", wrong_format, ". (", arr[i], ")");
                alert(res);
                return false;
            }
            arr[i] = +arr[i];
            if (arr[i] < 1 || arr[i] > length) {
                var res = test.concat(" 9. ", block_length_range_not_allowed, ". (", arr[i], ")");
                alert(res);
                return false;
            }
        }
    }

    if (document.getElementsByName("universal")[0].checked) {
        checked_any_test = true;
    }

    if (document.getElementsByName("apen")[0].checked) {
        checked_any_test = true;
        var param_array = document.getElementsByName("linear_param")[0].value;
        if (param_array.length == 0)
            return true;
        var boundary = Math.floor(Math.log(length) / Math.log(2)) - 6;
        for(var i=0; i<arr.length; i++) {
            if (isNaN(arr[i])) {
                var res = test.concat(" 2. ", wrong_format, ". (", arr[i], ")");
                alert(res);
                return false;
            }
            arr[i] = +arr[i];
            if (arr[i] > boundary) {
                var res = test.concat(" 11. ", block_length_range_not_allowed, ". (", arr[i], ")");
                alert(res);
                return false;
            }
        }
    }

    if (document.getElementsByName("excursion")[0].checked) {
        checked_any_test = true;
        if (length < 1000000) {
            var res = test.concat(" 12. ", length_range_not_allowed);
            alert(res);
            return false;
        }
    }

    if (document.getElementsByName("excursion_var")[0].checked) {
        checked_any_test = true;
        if (length < 1000000) {
            var res = test.concat(" 13. ", length_range_not_allowed);
            alert(res);
            return false;
        }
    }

    if (document.getElementsByName("serial")[0].checked) {
        checked_any_test = true;
        var param_array = document.getElementsByName("linear_param")[0].value;
        if (param_array.length == 0)
            return true;
        var boundary = Math.floor(Math.log(length) / Math.log(2)) - 3;
        for(var i=0; i<arr.length; i++) {
            if (isNaN(arr[i])) {
                var res = test.concat(" 2. ", wrong_format, ". (", arr[i], ")");
                alert(res);
                return false;
            }
            arr[i] = +arr[i];
            if (arr[i] < 3 || arr[i] > boundary) {
                var res = test.concat(" 14. ", block_length_range_not_allowed, ". (", arr[i], ")");
                alert(res);
                return false;
            }
        }
    }

    if (document.getElementsByName("linear")[0].checked) {
        checked_any_test = true;
        if (length <= 1000000) {
            var res = test.concat(" 15. ", length_range_not_allowed);
            alert(res);
            return false;
        }

        var param_array = document.getElementsByName("linear_param")[0].value;
        if (param_array.length == 0)
            return true;
        var arr = param_array.split(',');
        for(var i=0; i<arr.length; i++) {
            if (isNaN(arr[i])) {
                var res = test.concat(" 2. ", wrong_format, ". (", arr[i], ")");
                alert(res);
                return false;
            }
            arr[i] = +arr[i];
            if (arr[i] < 500 || arr[i] > 5000) {
                var res = test.concat(" 15. ", block_length_range_not_allowed, ". (", arr[i], ")");
                alert(res);
                return false;
            }
        }
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