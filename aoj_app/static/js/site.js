function ajax_loading_modal(tf) {
    if (tf) {
        $('body').addClass("loading");
    } else {
        $('body').removeClass("loading");
    }
}

$(function () {
// MMENU
    $("nav#mobile-menu").mmenu({
        "offCanvas": {
            "position": "right"
        }
    });

// FANCYBOX IN CATALOGUE
    $('.fancy-image').fancybox();

// ADD TO CART
    $('.btn-add-to-cart').click(function () {
        add_to_cart($(this).data('id'));
    });

    function add_to_cart(product_id) {
        ajax_loading_modal(true);
        $.get('/api/add_to_cart/', {product_id: product_id}, function (e) {
            if (e['error'] === 0) {
                // Change CART(x) val in the nav
                $('#cart-items-count').html(e['count'] > 0 ? '(' + e['count'] + ')' : '');
                // Add IN CART text to box
                $('.in-cart[data-id="' + product_id + '"]').html('IN CART (x' + e['qty'] + ')');
            }
        }).always(function (e) {
            ajax_loading_modal(false);
        });
    }

// REMOVE FROM CART
    $('.btn-remove-from-cart').click(function () {
        remove_from_cart(this, $(this).data('id'));
    });

    function remove_from_cart(el, product_id) {
        ajax_loading_modal(true);
        $.get('/api/remove_from_cart/', {product_id: product_id}, function (e) {
            if (e['error'] === 0) {
                $(el).closest('tr').fadeOut("fast", function () {
                    $(this).remove();
                    // Change CART(x) val in the nav
                    $('#cart-items-count').html(e['count'] > 0 ? '(' + e['count'] + ')' : '');
                    // Change total value
                    $('#cart-total').html(e['total']);
                })
            }
        }).always(function (e) {
            ajax_loading_modal(false);
        });
        ;
    }

// CHANGE QUANTITY
    $('.cart-qty-input').change(function () {
        product_change_quantity($(this).data('id'), $(this).val());
    });

    function product_change_quantity(product_id, qty) {
        ajax_loading_modal(true);
        $.get('/api/product_change_quantity/', {product_id: product_id, qty: qty}, function (e) {
            if (e['error'] === 0) {
                // Change CART(x) val in the nav
                $('#cart-items-count').html(e['count'] > 0 ? '(' + e['count'] + ')' : '');
                // Change input val with a val returned
                $('.cart-qty-input[data-id="' + product_id + '"]').val(e['qty']);
                // Change subtotal in item
                $('.cart-subtotal[data-id="' + product_id + '"]>span').html(e['item_subtotal']);
                // Change total value
                $('#cart-total').html(e['total']);
            }
        }).always(function (e) {
            ajax_loading_modal(false);
        });
    }

// INCREMENT QTY
    $('.btn-qty-inc').click(function () {
        product_increment_quantity($(this).data('id'));
    });

    function product_increment_quantity(product_id) {
        ajax_loading_modal(true);
        $.get('/api/product_increment_quantity/', {product_id: product_id}, function (e) {
            if (e['error'] === 0) {
                // Change CART(x) val in the nav
                $('#cart-items-count').html(e['count'] > 0 ? '(' + e['count'] + ')' : '');
                // Change input val with a val returned
                $('.cart-qty-input[data-id="' + product_id + '"]').val(e['qty']);
                // Change subtotal in item
                $('.cart-subtotal[data-id="' + product_id + '"]>span').html(e['item_subtotal']);
                // Change total value
                $('#cart-total').html(e['total']);
            }
        }).always(function (e) {
            ajax_loading_modal(false);
        });
    }

// DECREMENT QTY
    $('.btn-qty-dec').click(function () {
        product_decrement_quantity($(this).data('id'));
    });

    function product_decrement_quantity(product_id) {
        ajax_loading_modal(true);
        $.get('/api/product_decrement_quantity/', {product_id: product_id}, function (e) {
            if (e['error'] === 0) {
                // Change CART(x) val in the nav
                $('#cart-items-count').html(e['count'] > 0 ? '(' + e['count'] + ')' : '');
                // Change input val with a val returned
                $('.cart-qty-input[data-id="' + product_id + '"]').val(e['qty']);
                // Change subtotal in item
                $('.cart-subtotal[data-id="' + product_id + '"]>span').html(e['item_subtotal']);
                // Change total value
                $('#cart-total').html(e['total']);
            }
        }).always(function (e) {
            ajax_loading_modal(false);
        });
    }

// POPULATE SHIP FIELDS IN THE CHECKOUT FORM
    $('#form-checkout').submit(function () {
        $(this).find('input[type="submit"]').attr('disabled', 'disabled');

        // First name
        $(this).find('input[name="x_ship_to_first_name"]').val($(this).find('input[name="x_first_name"]').val());
        // Last name
        $(this).find('input[name="x_ship_to_last_name"]').val($(this).find('input[name="x_last_name"]').val());
        // Address
        $(this).find('input[name="x_ship_to_address"]').val($(this).find('input[name="x_address"]').val());
        // City
        $(this).find('input[name="x_ship_to_city"]').val($(this).find('input[name="x_city"]').val());
        // State
        $(this).find('input[name="x_ship_to_state"]').val($(this).find('input[name="x_state"]').val());
        // Zip
        $(this).find('input[name="x_ship_to_zip"]').val($(this).find('input[name="x_zip"]').val());
        // Country
        $(this).find('input[name="x_ship_to_country"]').val($(this).find('input[name="x_country"]').val());

        // SEND EMAIL BEFORE SUBMITTING THE FORM
        $.ajax({
            method: "POST",
            url: "/api/send_checkout_form/",
            data: $(this).serialize(),
            async: false,
            timeout: 30000,
        }).done(function (data) {
            $('#form-checkout input[name="x_fp_timestamp"]').val(data["x_fp_timestamp"]);
            $('#form-checkout input[name="x_fp_hash"]').val(data["x_fp_hash"]);
            return true;
        }).fail(function () {
            return false;
        });
    });

// CALCULATE X_FP_HASH FOR THE DONATE FORM
    $('#cbfAmount').change(function () {
        if ($(this).val() != 'other') {
            $('.oa').slideUp();
            $('#cbfOA').prop('required', false);
            $('input[name="x_amount"]').val($(this).val());
            calculate_fp_hash();
        } else {
            $('#cbfOA').val($('input[name="x_amount"]').val());
            $('.oa').slideDown();
            $('#cbfOA').prop('required', true);
        }
    });

    $('#cbfOA').change(function () {
        $('input[name="x_amount"]').val($(this).val());
        calculate_fp_hash();
    });

    function calculate_fp_hash() {
        ajax_loading_modal(true);
        var x_login = $('#form-donate').find('input[name="x_login"]').val();
        var x_fp_sequence = $('#form-donate').find('input[name="x_fp_sequence"]').val();
        var x_amount = $('#form-donate').find('input[name="x_amount"]').val();
        var x_currency_code = $('#form-donate').find('input[name="x_currency_code"]').val();
        $.get('/api/calculate_fp_hash/',
            {
                x_login: x_login, x_fp_sequence: x_fp_sequence, x_amount: x_amount,
                x_currency_code: x_currency_code
            },
            function (e) {
                if (e['error'] === 0) {
                    $('#form-donate').find('input[name="x_amount"]').val(e['x_amount']);
                    $('#form-donate').find('input[name="x_fp_hash"]').val(e['x_fp_hash']);
                }
            }).always(function (e) {
            ajax_loading_modal(false);
        });
    }

// SEND EMAIL BEFORE SUBMIT DONATE FORM
    $('#form-donate').submit(function (e) {
        $('#form-donate input[type="submit"]').attr('disabled', 'disabled');
        $.ajax({
            method: "POST",
            url: "/api/send_donate_form/",
            data: $('#form-donate').serialize(),
            async: false,
            timeout: 30000,
        }).done(function (data) {
            $('#form-donate input[name="x_fp_timestamp"]').val(data["x_fp_timestamp"]);
            $('#form-donate input[name="x_fp_hash"]').val(data["x_fp_hash"]);
            return true;
        }).fail(function () {
            return false;
        });
    });


// VALIDATE CHILDREN SPONSORSHIP FORM
    $('#form-child-sponsorship').validate({
        rules: {
            first_name: {
                required: true,
                minlength: 2
            },
            last_name: {
                required: true,
                minlength: 2
            },
            address: {
                required: true,
                minlength: 2
            },
            city: {
                required: true,
                minlength: 2
            },
            state: {
                required: true,
                minlength: 2
            },
            zip: {
                required: true,
                minlength: 2
            },
            country: {
                required: true,
                minlength: 2
            },
            email: {
                required: true,
                email: true
            },
            phone: {
                required: true,
                minlength: 2
            }
        },
        messages: {
            first_name: {
                required: "This field is required",
                minlength: "This field must consist of at least 2 characters"
            },
            last_name: {
                required: "This field is required",
                minlength: "This field must consist of at least 2 characters"
            },
            address: {
                required: "This field is required",
                minlength: "This field must consist of at least 2 characters"
            },
            city: {
                required: "This field is required",
                minlength: "This field must consist of at least 2 characters"
            },
            state: {
                required: "This field is required",
                minlength: "This field must consist of at least 2 characters"
            },
            zip: {
                required: "This field is required",
                minlength: "This field must consist of at least 2 characters"
            },
            country: {
                required: "This field is required",
                minlength: "This field must consist of at least 2 characters"
            },
            email: {
                required: "This field is required"
            },
            phone: {
                required: "This field is required",
                minlength: "This field must consist of at least 2 characters"
            }
        },
        submitHandler: function (form) {
            ajax_loading_modal(true);
            $(form).find('button[type="submit"]').attr('disabled', true);
            $.ajax({
                method: "POST",
                url: "/api/send_sponsorship_form/",
                data: $(form).serialize()
            }).done(function (e) {
                if (e['error'] === 0) {
                    $(form).fadeTo("slow", 0.15, function () {
                        $('.form-wrapper .f-success').fadeIn('slow');
                    });
                } else {
                    $(form).fadeTo("slow", 0.15, function () {
                        $('.form-wrapper .f-error').fadeIn('slow');
                    });
                }
            }).fail(function () {
                $(form).fadeTo("slow", 0.15, function () {
                    $('.form-wrapper .f-error').fadeIn('slow');
                });
            }).always(function () {
                ajax_loading_modal(false);
                //$(form).find('button[type="submit"]').attr('disabled', true);
            });
        }
    });


// VALIDATE CONTACT FORM
    $('#form-contact').validate({
        rules: {
            first_name: {
                required: true,
                minlength: 2
            },
            last_name: {
                required: true,
                minlength: 2
            },
            email: {
                required: true,
                email: true
            },
            message: {
                required: true,
                minlength: 2
            }
        },
        messages: {
            first_name: {
                required: "This field is required",
                minlength: "This field must consist of at least 2 characters"
            },
            last_name: {
                required: "This field is required",
                minlength: "This field must consist of at least 2 characters"
            },
            email: {
                required: "This field is required"
            },
            message: {
                required: "This field is required",
                minlength: "This field must consist of at least 2 characters"
            }
        },
        submitHandler: function (form) {
            ajax_loading_modal(true);
            $(form).find('input[type="submit"]').attr('disabled', true);
            $.ajax({
                // method: "POST",
                type:"POST",
                url: "/api/send_contact_form/",
                data: $(form).serialize()
            }).done(function (e) {
                if (e['error'] === 0) {
                    $(form).fadeTo("slow", 0.15, function () {
                        $('.form-wrapper .f-success').fadeIn('slow');
                    });
                } else {
                    $(form).fadeTo("slow", 0.15, function () {
                        $('.form-wrapper .f-error').fadeIn('slow');
                    });
                }
            }).fail(function () {
                $(form).fadeTo("slow", 0.15, function () {
                    $('.form-wrapper .f-error').fadeIn('slow');
                });
            }).always(function () {
                //$(form).find('button[type="submit"]').attr('disabled', true);
                ajax_loading_modal(false);
            });
        }
    });

});