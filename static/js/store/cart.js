/**
 * Created by allen on 16/8/26.
 */
require(["jquery", "bsAlert", "csrfToken"], function ($, bsAlert, csrfTokenHeader) {
    $('.qtyplus').click(function (e) {
        e.preventDefault();
        var count_item = $(this).parents('td');
        var cart_item = count_item.parent();
        var cart_id = parseInt(cart_item.attr('cart_id'));
        var quantity_input = count_item.find('.qty');
        $.ajax({
                beforeSend: csrfTokenHeader,
                url: "/cartnum_op/",
                data: {
                    cart_id:cart_id,
                    is_add: true,
                },
                dataType: "json",
                method: "post",
                success: function (data) {
                    if (!data.code) {
                       var res_num = data.data.res_num;
                        var total_price = data.data.total_price;
                        var item_price = data.data.item_price;
                        quantity_input.val(res_num);
                        count_item.next('td').next('td').text(item_price+"元");
                        $('#total_price').text("总价 "+total_price+"元");
                    }
                    else {
                        bsAlert(data.data);
                    }
                },
                error: function(){
                    bsAlert("额 好像出错了，请刷新页面重试。如还有问题，请填写页面导航栏上的反馈。")
                }
            });
    });

    $('.qtyminus').click(function (e) {
        e.preventDefault();
        var count_item = $(this).parents('td');
        var cart_item = count_item.parent();
        var cart_id = parseInt(cart_item.attr('cart_id'));
        var quantity_input = count_item.find('.qty');
        $.ajax({
                beforeSend: csrfTokenHeader,
                url: "/cartnum_op/",
                data: {
                    cart_id:cart_id,
                    is_add: false,
                },
                dataType: "json",
                method: "post",
                success: function (data) {
                    if (!data.code) {
                        var res_num = data.data.res_num;
                        var total_price = data.data.total_price;
                        var item_price = data.data.item_price;
                        if (res_num == 0){
                            cart_item.hide();
                        }
                        else{
                            quantity_input.val(res_num);
                            count_item.next('td').next('td').text(item_price+"元");
                            $('#total_price').text("总价 "+total_price+"元");
                        }
                    }
                    else {
                        bsAlert(data.data);
                    }
                },
                error: function(){
                    bsAlert("额 好像出错了，请刷新页面重试。如还有问题，请填写页面导航栏上的反馈。")
                }
            });
    });

    $('.delete_cart_item').click(function (e) {
        e.preventDefault();
        var cart_item = $(this).parents('tr');
        var cart_id = parseInt(cart_item.attr('cart_id'));
        $.ajax({
                beforeSend: csrfTokenHeader,
                url: "/delete_cart_item/",
                data: {
                    cart_id:cart_id,
                },
                dataType: "json",
                method: "post",
                success: function (data) {
                    if (!data.code) {
                        cart_item.hide();
                        var total_price = data.data;
                        $("#total_price").text("总价"+total_price+"元");
                    }
                    else {
                        bsAlert(data.data);
                    }
                },
                error: function(){
                    bsAlert("额 好像出错了，请刷新页面重试。如还有问题，请填写页面导航栏上的反馈。")
                }
            });
    });

    $('.clear_cart').click(function (e) {
        e.preventDefault();
        $.ajax({
                beforeSend: csrfTokenHeader,
                url: "/clear_cart/",
                data: {
                },
                dataType: "json",
                method: "post",
                success: function (data) {
                    if (!data.code) {
                        $(".cart_item").hide();
                        $("#total_price").text("总价0.0元");
                    }
                    else {
                        bsAlert(data.data);
                    }
                },
                error: function(){
                    bsAlert("额 好像出错了，请刷新页面重试。如还有问题，请填写页面导航栏上的反馈。")
                }
            });
    });
});