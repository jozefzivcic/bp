function validateForm() {
    var length = parseInt(document.getElementsByName("length")[0].value);
    var streams = parseInt(document.getElementsByName("streams")[0].value);
    var test = document.getElementsByName("test")[0].value;
    var length_range_not_allowed = document.getElementsByName("length_range_not_allowed")[0].value;
    var block_length_range_not_allowed = document.getElementsByName("block_length_range_not_allowed")[0].value;
    var wrong_format = document.getElementsByName("wrong_format")[0].value;
    var checked_any_test = false;

    if (!checkFiles(length, streams))
        return false;

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
        var arr = document.getElementsByName("block_frequency_param")[0].value.split(',');
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
    if (document.getElementsByName("overlapping")[0].checked) {
        checked_any_test = true;
        var arr = document.getElementsByName("overlapping_param")[0].value.split(',');
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

    if (document.getElementsByName("apen")[0].checked) {
        checked_any_test = true;
        var arr = document.getElementsByName("apen_param")[0].value.split(',');
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

        if (length < 1000000) {
            var res = test.concat(" 13. ", length_range_not_allowed);
            alert(res);
            return false;
        }
    }

    if (document.getElementsByName("serial")[0].checked) {
        checked_any_test = true;
        var arr = document.getElementsByName("serial_param")[0].value.split(',');
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

        var arr = document.getElementsByName("linear_param")[0].value.split(',');
        for(var i=0; i<arr.length; i++) {
            if (isNaN(arr[i])) {
                var res = test.concat(" 2. ", wrong_format, ". (", arr[i], ")");
                alert(res);
                return false;
            }
            arr[i] = +arr[i];
            if (arr[i] < 500 || arr[i] > 5000) {
                var res = test.concat(" 14. ", block_length_range_not_allowed, ". (", arr[i], ")");
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
    var eles = [];
    var inputs = document.getElementsByTagName("input");
    for(var i = 0; i < inputs.length; i++) {
        if(inputs[i].name.indexOf('file') == 0) {
            eles.push(inputs[i]);
        }
    }
}